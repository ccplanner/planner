;; defineing chips challenge domain
;; very simple

(define (domain chips-challenge)
  (:requirements :typing )
  (:types thing location direction number - object
          player - thing)
  (:predicates (floor ?l - location)
               (at ?t - thing ?l - location)
               (chip ?l - location)
               (socket ?l - location)
               (wall ?l - location)
               (successor ?n1 - number ?n0 - number)
               (chips-left ?n - number)
               (MOVE-DIR ?from ?to - location ?dir - direction))

  (:action move-floor
   :parameters (?p - player ?from ?to - location ?dir - direction)
   :precondition (and (at ?p ?from)
                      (floor ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      )
   :effect       (and (not (at ?p ?from))
                      (at ?p ?to)
                      )
   )
  
  (:action move-socket
   :parameters (?p - player ?from ?to - location ?dir - direction)
   :precondition (and (at ?p ?from)
                      (socket ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (chips-left n0)
                      )
   :effect       (and (not (at ?p ?from))
                      (at ?p ?to)
                      (not (socket ?to))
                      (floor ?to)
                      )
   )

;; handle having n0 chips
;; maybe make zero a succesor to itself
  (:action move-chip
   :parameters (?p - player ?from ?to - location ?dir - direction ?ochips ?nchips - number)
   :precondition (and (at ?p ?from)
                      (chip ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (chips-left ?ochips)
                      (successor ?nchips ?ochips)
                      )
   :effect       (and (not (at ?p ?from))
                      (at ?p ?to)
                      (not (chip ?to))
                      (floor ?to)
                      (not (chips-left ?ochips))
                      (chips-left ?nchips)
                      )
   )
)
