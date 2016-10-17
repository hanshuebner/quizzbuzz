(ns quizzbuzz.server
  (:gen-class)
  (:require [clojure.java.io :as io]
            [dk.ative.docjure.spreadsheet :as spreadsheet]
            [ring.middleware.json :refer [wrap-json-response]]
            [ring.middleware.keyword-params :refer [wrap-keyword-params]]
            [ring.middleware.params :refer [wrap-params]]
            [ring.util.response :as response]
            [ring.adapter.jetty :refer [run-jetty]]
            [compojure.core :refer :all]
            [compojure.route :as route]
            [me.raynes.fs :as fs]
            [clojure.string :as string]))

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

(defn load-questions-from-excel [resource-name]
  (->> (spreadsheet/load-workbook-from-resource resource-name)
       spreadsheet/sheet-seq
       first
       (spreadsheet/select-columns {:B :question
                                    :C :answer-correct
                                    :D :answer-incorrect-1
                                    :E :answer-incorrect-2
                                    :F :answer-incorrect-3
                                    :G :level
                                    :H :category})
       rest
       (map normalize-question)))

(defn catego-and-randomize [questions]
  (->> questions
       shuffle
       (group-by :category)))

(defn questions-upto-level [questions max-level]
  (filter #(<= (:level %) max-level) questions))

(defn categories-with-questions [database question-count max-level]
  (filter (fn [category]
            (>= (count (questions-upto-level (database category) max-level)) question-count))
          (keys database)))

(defn get-questions [database category question-count max-level]
  (let [questions-chosen (take question-count (questions-upto-level (database category) max-level))]
    [questions-chosen
     (update database category (partial remove (set questions-chosen)))]))

(defn statistics [resource-name]
  (->> (load-questions-from-excel resource-name)
       (group-by :category)
       (map (fn [[category questions]]
              [category (frequencies (map :level questions))]))
       (into {})))

(defn known-categories [database]
  (set (keys database)))

(defn parse-params [{:keys [question-count max-level] :as params}]
  (assoc params
         :question-count (if question-count
                           (Integer/parseInt question-count)
                           10)
         :max-level (if max-level
                      (Integer/parseInt max-level)
                      10)))

(defn get-questions-handler [{:keys [params config database]}]
  (let [{:keys [questions-resource-name]} config
        {:keys [max-level category question-count]} (parse-params params)]
    (cond
      (not (<= 1 max-level 10))
      (-> (response/response "invalid max-level")
          (response/status 400))

      (not (get (known-categories database) category))
      (-> (response/response "invalid category")
          (response/status 400))

      :otherwise
      (let [[questions database] (get-questions database
                                                category
                                                question-count
                                                max-level)]
        (if (seq questions)
          (assoc (response/response questions)
                 :database database)
          (response/not-found "no matching questions found"))))))

(defn get-categories-handler [{:keys [database params]}]
  (let [{:keys [max-level question-count]} (parse-params params)]
    (response/response (categories-with-questions database question-count max-level))))

(defn load-database [database-file]
  (if (fs/exists? database-file)
    (read-string (slurp database-file))
    (-> (load-questions-from-excel "2500-Fragen.xlsx")
        catego-and-randomize)))

(defn wrap-database [handler]
  (fn [{:keys [headers] :as request}]
    (if-let [client-id (get headers "x-client-id")]
      (let [database-file (fs/file "database" (string/replace client-id #"(?i)[^a-z0-9-]" ""))
            response (handler (assoc request
                                     :database (load-database database-file)))]
        (when-let [database (:database response)]
          (spit database-file (pr-str database)))
        (dissoc response :database))
      (-> (response/response "missing X-Client-ID header")
          (response/status 400)))))

(defroutes app
  (POST "/questions" [] get-questions-handler)
  (GET "/categories" [] get-categories-handler)
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
                                 wrap-database)
                             {:port port
                              :join? false}))))

(defn -main []
  (run-server)
  (.join @server))
