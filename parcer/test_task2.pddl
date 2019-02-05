(define (problem elevators-sequencedstrips-p8_3_1)
(:domain elevators-sequencedstrips)

(:objects 
s1 s2 s3  - slow-car
f1 f2 f3  - fast-car
c1 c2 c3 - city
p1 p2 - passenger
)

(:init


(passenger-at p1 c1)    (passenger-at p2 c3)         
(car-at s1 c1) (car-at s2 c1) (car-at s3 c1)
(car-at f1 c1) (car-at f2 c1) (car-at f3 c1)          


(far-town c1)
(near-town c2)
(main-town c3)    



)

(:goal (long-travel f1 c1 c2 c3) )
