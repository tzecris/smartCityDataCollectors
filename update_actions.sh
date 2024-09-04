    wsk property set --auth '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'

    echo "Updating actions"
    wsk -i action update cowa --docker tzelishua/collectorow:latest collectorOpenWeather/__main__.py
    wsk -i action update zipcollect --docker tzelishua/openwhiskdactions:latest collectorFromZipFiles/__main__.py 
    wsk -i action update zipprocess --docker tzelishua/openwhiskdactions:latest processorFromZipFiles/__main__.py 
    wsk -i action update getWeatherInfo --docker tzelishua/collectorow:latest currentWeatherFromAddress/__main__.py 
    wsk -i action update read_data --docker tzelishua/collectorow:latest readFromDB/__main__.py 
    wsk -i action update processow --docker tzelishua/collectorow:latest processorOpenWeather/__main__.py
    wsk -i action update weatherNotify --docker tzelishua/collectorow:latest weatherNotification/__main__.py
    wsk -i action update weatherPredict --docker tzelishua/collectorow:latest weatherPrediction/__main__.py



    echo "Updating sequence"
    wsk -i action update mySequence --sequence zipcollect,zipprocess