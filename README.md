# lora
Simple lora trillateration visualisation

Install:
* Create database in mysql with data/load.sql
* Fill database with sample data using python/insertSamples.py
* Create config.php based on config.php.sample
* Place config.php and get.php into HTTP server
* Create config.py based on config.py.sample
* Run insertSamples.sh to insert sample data
* Fix the samples with coordinates (manually with UPDATE)
* Run npm install to get node.js modules
* Change in main.js serviceUrl: "http://localhost/lora/get.php"
* Run python/run.sh to have realtime simulation
* Run npm run serve

This should lead into web available at http://localhost:8081/ or http://localhost:8080/

Build for production:
* Run npm run build