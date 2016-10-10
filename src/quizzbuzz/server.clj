(ns quizzbuzz.server
  (:require [clojure.java.io :as io]
            [dk.ative.docjure.spreadsheet :as spreadsheet]
            [ring.middleware.json :refer [wrap-json-response]]
            [ring.middleware.keyword-params :refer [wrap-keyword-params]]
            [ring.middleware.params :refer [wrap-params]]
            [ring.util.response :as response]
            [ring.adapter.jetty :refer [run-jetty]]
            [compojure.core :refer :all]
            [compojure.route :as route]))

(defn ensure-string [thing]
  (if (float? thing)
    (format "%.0f" thing)
    thing))

(defn normalize-question [{:keys [answer-correct answer-incorrect-1 answer-incorrect-2 answer-incorrect-3 level]
                           :as question}]
  (into question
        {:answer-correct (ensure-string answer-correct)
         :answer-incorrect-1 (ensure-string answer-incorrect-1)
         :answer-incorrect-2 (ensure-string answer-incorrect-2)
         :answer-incorrect-3 (ensure-string answer-incorrect-3)
         :level (int level)}))

(def get-questions
  (memoize (fn [resource-name]
             (->> (spreadsheet/load-workbook-from-resource resource-name)
                  (spreadsheet/select-sheet "Tabelle1")
                  (spreadsheet/select-columns {:A :question
                                               :B :answer-correct
                                               :C :answer-incorrect-1
                                               :D :answer-incorrect-2
                                               :E :answer-incorrect-3
                                               :F :level
                                               :G :category})
                  rest
                  (map normalize-question)))))

(defn get-question
  ([resource-name]
   (get-question resource-name {}))
  ([resource-name {:keys [level category]}]
   (let [wanted (fn [question]
                  (and (or (not level)
                           (= level (:level question)))
                       (or (not category)
                           (= category (:category question)))))]
     (->> (get-questions resource-name)
          (filter wanted)
          seq
          rand-nth))))

(defn statistics [resource-name]
  (->> (get-questions resource-name)
       (group-by :category)
       (map (fn [[category questions]]
              [category (frequencies (map :level questions))]))
       (into {})))

(defn known-categories [resource-name]
  (-> (statistics resource-name)
      keys
      set))

(defn get-question-handler [{:keys [params config]}]
  (let [{:keys [questions-resource-name]} config
        {:keys [level category]} params
        level (and level (Integer/parseInt level))]
    (cond
      (and level
           (not (<= 1 level 3)))
      (-> (response/response "invalid level")
          (response/status 400))

      (and category
           (not (get (known-categories questions-resource-name) category)))
      (-> (response/response "invalid category")
          (response/status 400))

      :otherwise
      (if-let [question (get-question questions-resource-name
                                      {:level level
                                       :category category})]
        (response/response question)
        (response/not-found "no matching question found")))))

(defroutes app
  (POST "/question" [] get-question-handler)
  (route/not-found "page not found"))

(defonce server (atom nil))

(defn run-server
  ([]
   (run-server {}))
  ([{:keys [port]
     :or {port 3399}}]
   (if @server
     (.stop @server))
   (reset! server (run-jetty (-> app
                                 wrap-json-response
                                 wrap-keyword-params
                                 wrap-params
                                 wrap-config)
                             {:port port
                              :join? false}))))
