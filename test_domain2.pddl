;;;
;;
;;;


(define (domain elevators-sequencedstrips)
  (:requirements :something :something2)
  (:types 	car - object 
		slow-car fast-car - elevator
   		passenger - object
          	city
         )

(:predicates 
	(passenger-at ?person - passenger ?c - city)
	(boarded ?person - passenger ?c1 - car)
	(car-at ?c - car ?town - city)
	(empty ?c car)
	(far-town ?t city)
	(near-town ?t city)
	(main-town ?t city)
)

(:- (main-town ?c) (and (not (far-town ?c)) (not (near-town ?c))))
(:- (near-town ?c) (and (not (main-town ?c)) (not (far-town ?c))))
(:- (far-town ?c) (and (not (main-town ?c)) (not (near-town ?c))))

(:operator
	(near-travel ?a ?b - city ?c - car)
	(and (not (main-town ?a)) (not (main-town ?b)))
	(and (car-at ?c ?a) (not (car-at ?c ?b)))
)

(:operator
	(near-travel2 ?a ?b - city ?c - car)
	(and (not (far-town ?a)) (not (far-town ?b)))
	(and (car-at ?c ?a) (not (car-at ?c ?b)))
)

(:operator
	(seat ?a - person ?c - car)
	(and (empty ?c) (not (boarded a? c?)))
	(and (boarded a? c?) (not (empty ?c)))
)

(:method
	(long-travel ?c - car ?c1 ?c2 ?c3 - city)
	(and (not (near-town ?c1)) (not (near-town ?c2)))
	(:ordered (near-travel ?c1 ?c2) (near-travel ?c2 ?c3))
)


  
)

