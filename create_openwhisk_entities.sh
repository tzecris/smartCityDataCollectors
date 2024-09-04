
    wsk property set --auth '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'

    
    echo "Creating actions"
    wsk -i action create cowa --docker tzelishua/collectorow:latest collectorOpenWeather/__main__.py
    wsk -i action create zipcollect --docker tzelishua/openwhiskdactions:latest collectorFromZipFiles/__main__.py 
    wsk -i action create zipprocess --docker tzelishua/openwhiskdactions:latest processorFromZipFiles/__main__.py 
    wsk -i action create getWeatherInfo --docker tzelishua/collectorow:latest currentWeatherFromAddress/__main__.py 
    wsk -i action create read_data --docker tzelishua/collectorow:latest readFromDB/__main__.py 
    wsk -i action create processow --docker tzelishua/collectorow:latest processorOpenWeather/__main__.py 
    wsk -i action create weatherNotify --docker tzelishua/collectorow:latest weatherNotification/__main__.py
    wsk -i action create weatherPredict --docker tzelishua/collectorow:latest weatherPrediction/__main__.py
   
       
    echo "Creating trigger"
    wsk -i trigger create periodic   --feed /whisk.system/alarms/alarm   --param cron "*/5 * * * *" 
    wsk -i trigger create periodicDaily   --feed /whisk.system/alarms/alarm   --param cron "0 0 * * *" 
    
    echo "Creating rules"
    wsk -i rule create collectorOWrule periodic cowa
    wsk -i rule create proccessDailyRule periodicDaily processow

    echo "Creating sequence"
    wsk -i action create mySequence --sequence zipcollect,zipprocess
    

