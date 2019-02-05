;;;
;; comments
;;;


(define (domain test1)
  (:requirements :something :something2)
  (:types 	object place)

(:predicates 
	(on ?o1 ?o2 - object)
	(in ?o1 - object ?p1 - place)
)



(:operator
	(do-smth ?a ?b - object)
	(and (on ?a ?b) (not (on ?b ?a)))
	(and (on ?b ?a) (not (on ?a ?b)))
)

(:operator
	(do-things ?a - object ?b - place)
	(and (in ?a ?b) (not (in ?b ?a)))
	(and (in ?b ?a) (not (in ?a ?b)))
)

  
)

