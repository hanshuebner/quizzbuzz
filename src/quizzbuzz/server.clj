(ns quizzbuzz.server
  (:require [clojure.java.io :as io]
            [dk.ative.docjure.spreadsheet :as spreadsheet]
            [ring.middleware.json :refer [wrap-json-response]]
            [ring.util.response :refer [response]]
            [ring.adapter.jetty :refer [run-jetty]]))

(defn get-question [resource-name]
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
       rand-nth))

(defn get-question-handler [request]
  (response (get-question "FragenAuswahl.xlsx")))

(def app
  (wrap-json-response get-question-handler))

(defn run-server [{:keys [port]
                   :or {port 3399}}]
  (run-jetty app
             {:port port}))
