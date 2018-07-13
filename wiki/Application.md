# Applications

## Intel Joule Movidius Demo:

#### Caffe with SSD mobileNet -> video object detection
Results are:
- 1. Video:contrapicado_traffic_shortened_960x540.mp4. video resolution: 960.0 x 540.0
  - CPU Per: 23.3669340974
  - Mem Average: 85442271.4502
  - Frame Count:873
  - Second per frame:0.103543150193
- 2. Video:bus_station_6094_960x540.mp4. video resolution: 960.0 x 540.0
  - CPU Per: 23.548346763
  - Mem Average: 86995197.7244
  - Frame Count:927 
  - Second per frame:0.103673908446
- 3. Video:motorcycle_6098_shortened_960x540.mp4. video resolution: 960.0 x 540.0
  - CPU Per: 23.5804342523
  - Mem Average: 87253410.5912
  - Frame Count:250
  - Second per frame:0.104312363625
- 4. Video:police_car_6095_shortened_960x540.mp4. video resolution: 960.0 x 540.0
  - CPU Per: 23.4771455399
  - Mem Average: 87681657.7033
  - Frame Count:613
  - Second per frame:0.104503486129
- 5. Video:scooters_5638_shortened_960x540.mp4. video resolution: 960.0 x 540.0
  - CPU Per: 23.4268770035
  - Mem Average: 87827321.9541
  - Frame Count:301
  - Second per frame:0.104320315428

## Jetson

#### SSD MobileNet with PyTorch:
Results are: 
- 1. Video:contrapicado_traffic_shortened_960x540.mp4. video resolution: 960.0 x 540.0
  - Processing Time Per Frame: 1.0628144820258107s
- 2. Video:bus_station_6094_960x540.mp4. video resolution: 960.0 x 540.0
  - Processing Time Per Frame: 2.1887673853284717s
- 3. Video:motorcycle_6098_shortened_960x540.mp4. video resolution: 960.0 x 540.0
  - Processing Time Per Frame: 1.6702866859436034
- 4. Video:police_car_6095_shortened_960x540.mp4. video resolution: 960.0 x 540.0
  - Processing Time Per Frame: 1.235303331549366s
- 5. Video:scooters_5638_shortened_960x540.mp4. video resolution: 960.0 x 540.0
  - Processing Time Per Frame: 1.005342649066963s


