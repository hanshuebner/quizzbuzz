(defproject quizzbuzz-server "0.1.0-SNAPSHOT"
  :description "quizzbuzz server"
  :main quizzbuzz.server
  :profiles {:uberjar {:aot :all
                       :uberjar-name "quizzbuz.jar"}}
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}
  :dependencies [[org.clojure/clojure "1.9.0-alpha12"]
                 [dk.ative/docjure "1.11.0"]
                 [ring "1.5.0"]
                 [ring/ring-json "0.4.0"]
                 [compojure "1.5.1"]
                 [alandipert/enduro "1.2.0"]
                 [me.raynes/fs "1.4.6"]])
