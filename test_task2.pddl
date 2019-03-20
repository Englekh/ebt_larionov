(define (problem test1-1)
(:domain test1)

(:objects 
o1 o2 o3 - object
p1 p2 p3 p4 p5 - place
r rr - robot
)

(:init

(on o1 p2)
(on o2 p3)
(on o3 p5)

(r_in r p1)
(r_in rr p4)

(same p1 p1)
(same p2 p2)
(same p3 p3)
(same p4 p4)
(same p5 p5)

)

(:goal  (get_two p2 p3 p1 o1 o2 r)
        (get_from p5 p4 o3 rr)
)


)
