(define (problem test1-1)
(:domain test1)

(:objects 
o1 o2 - object
p0 p1 p2 p3 p4 p5 - place
r1 r2 r3 - robot
)

(:init

(on o1 p2)
(on o2 p3)
(r_in r1 p1)
(r_in r2 p2)
(r_in r3 p4)

)

(:goal 	(go_to p1 p0 r1) 
	(go_to p2 p3 r2)
	(go_to p4 p5 r3)

)


)
