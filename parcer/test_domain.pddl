(define (domain test_domain)

	(:types         circle box - object
	                place
	                robot)

	(:predicates    (on ?o - object ?p - place)
	                (same ?p1 ?p2 - place)
	                (r_in ?r - robot ?p - place)
	                (got ?r - robot ?o - object)
	                (has_sth ?r - robot)
	)

	(:tasks         (get_from ?from ?now - place ?o - object ?r - robot)
	                (get_two ?from1 ?from2 ?now - place ?o1 ?o2 - object ?r - robot)
	                (go_to ?from ?to - place ?r - robot)
	                (take ?now - place ?o - object ?r - robot)
	                (lay ?now - place ?o - object ?r - robot)
	)


    (:operator      take    take_o
                    ((r_in ?now) (on ?o ?now) not (has_sth ?r) )
                    (not (on ?o ?now) (got ?o) (has_sth ?r) )
    )

    (:operator      lay    lay_o
                    (not (on ?o ?now) (got ?o) (has_sth ?r) )
                    ((r_in ?now) (on ?o ?now) not (has_sth ?r) )
    )

    (:operator      go_to    go_to_o
                    ((r_in ?r ?from) not (same ?from ?to) )
                    ((r_in ?r ?to) not (r_in ?r ?from) )
    )

    (:method        get_from go_and_take ordered 1
                    (not (same ?from ?now) (on ?o ?from) )
                    ((go_to ?now ?from ?r) (take ?from ?o ?r) (go_to ?from ?now ?r) (lay ?now ?o ?r) )
    )

    (:method        get_from do_nothing ordered 2
                    ((same ?from ?now) )
                    (() )
    )

    (:method        get_two divide ordered 2
                    ((on ?o1 ?from1) (on ?o2 ?from2) )
                    ((get_from ?from1 ?now ?o1 ?r) (get_from ?from2 ?now ?o2 ?r) )
    )

)
