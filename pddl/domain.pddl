;; defineing chips challenge domain
;; very simple

(define (domain chips-challenge)
  (:requirements :typing )
  (:types thing location direction number color - object
          player - thing)
  (:predicates (floor ?l - location)
               (at ?t - thing ?l - location)
               (chip ?l - location)
               (socket ?l - location)
               (wall ?l - location)
               (has-keys ?c - color ?n - number)
               (key ?l - location ?c - color)
               (door ?l - location ?c - color)
               (switch-wall-open ?l - location)
               (switch-wall-closed ?l - location)
               (switched-walls-open ?x - number )
               (successor ?n1 - number ?n0 - number)
               (chips-left ?n - number)
               (MOVE-DIR ?from ?to - location ?dir - direction))

  (:action move-floor
   :parameters (?p - player ?from ?to - location ?dir - direction)
   :precondition (and (at ?p ?from)
                      (floor ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (not (chip-state slipping))
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

;; Ice
  (:action move-ice
   :parameters (?p - player ?from ?to - location ?dir - direction)
   :precondition (and (at ?p ?from)
                      (ice ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (not (chip-state slipping))
                      )
   :effect       (and (not (at ?p ?from))
                      (at ?p ?to)
                      (chip-state slipping)
                      (slipping-dir ?dir)
                      )
   )

  (:action slip-ice-ice
   :parameters (?p - player ?from ?to - location ?dir - direction)
   :precondition (and (at ?p ?from)
                      (ice ?to)
                      (chip-state slipping)
                      (MOVE-DIR ?from ?to ?dir)
                      (slipping-dir ?dir)
                      )
   :effect       (and (not (at ?p ?from))
                      (at ?p ?to)
                      )
   )

  (:action slip-ice-floor
   :parameters (?p - player ?from ?to - location ?dir - direction)
   :precondition (and (at ?p ?from)
                      (floor ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (chip-state slipping)
                      (slipping-dir ?dir)
                      )
   :effect       (and (not (at ?p ?from))
                      (at ?p ?to)
                      (not (slipping-dir ?dir))
                      (not (chip-state slipping))
                      )
   )

  (:action slip-ice-chip
   :parameters (?p - player ?from ?to - location ?dir - direction ?ochips ?nchips - number)
   :precondition (and (at ?p ?from)
                      (chip ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (chips-left ?ochips)
                      (successor ?nchips ?ochips)
                      (chip-state slipping)
                      (slipping-dir ?dir)
                      )
   :effect       (and (not (at ?p ?from))
                      (at ?p ?to)
                      (not (chip ?to))
                      (floor ?to)
                      (not (chips-left ?ochips))
                      (chips-left ?nchips)
                      (not (slipping-dir ?dir))
                      (not (chip-state slipping))
                      )
   )

;; The switch walls
  (:action move-switch-wall-open
   :parameters (?p - player ?from ?to - location ?dir - direction)
   :precondition (and (at ?p ?from)
                      (switch-wall-open ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (switched-walls-open n0)
                      )
   :effect       (and (not (at ?p ?from))
                      (at ?p ?to)
                      )
   )

  (:action move-switch-wall-closed
   :parameters (?p - player ?from ?to - location ?dir - direction)
   :precondition (and (at ?p ?from)
                      (switch-wall-closed ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (not (switched-walls-open n0))
                      )
   :effect       (and (not (at ?p ?from))
                      (at ?p ?to)
                      )
   )

  (:action move-toggle-walls-open
   :parameters (?p - player ?from ?to - location ?dir - direction)
   :precondition (and (at ?p ?from)
                      (green-button ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (not (switched-walls-open n0))
                      )
   :effect       (and (not (at ?p ?from))
                      (at ?p ?to)
                      (switched-walls-open n0)
                      )
   )

  (:action move-toggle-walls-closed
   :parameters (?p - player ?from ?to - location ?dir - direction)
   :precondition (and (at ?p ?from)
                      (green-button ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (switched-walls-open n0)
                      )
   :effect       (and (not (at ?p ?from))
                      (at ?p ?to)
                      (not (switched-walls-open n0))
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

;; Keys

;; Move to a tile containing a ?color key, having had ?okeys ?color keys already.
;; TODO NOT TESTED
;; TODO Need to increase 'successor' numbers to accomodate large numbers of keys?
  (:action move-key
   :parameters (?p - player ?from ?to - location ?dir - direction ?color - color ?okeys ?nkeys - number)
   :precondition (and (at ?p ?from)
                      (key ?to ?color)
                      (MOVE-DIR ?from ?to ?dir)
                      (has-keys ?color ?okeys)
                      (successor ?okeys ?nkeys)
                      )
   :effect       (and (not (at ?p ?from))
                      (at ?p ?to)
                      (not (key ?to ?color))
                      (floor ?to)
                      (not (has-keys ?color ?okeys))
                      (has-keys ?color ?nkeys)
                      )
   )

;; Move to a tile containing a ?color door, having ?okeys ?color keys already.
;; TODO NOT TESTED
;; TODO Need to indicate to the planner special :requirement to handle 
;; the '=' or 'when' such as 'adl?  See 'benchmarks/psr-large/domain.pddl'
;; TODO Should colors be 'constants' instead of 'objects'?
  (:action move-door
   :parameters (?p - player ?from ?to - location ?dir - direction ?color - color ?okeys ?nkeys - number)
   :precondition (and (at ?p ?from)
                      (door ?to ?color)
                      (MOVE-DIR ?from ?to ?dir)
                      (has-keys ?color ?okeys)
                      (successor ?nkeys ?okeys)
                      (not (has-keys ?color n0))
                      )
   :effect       (and (not (at ?p ?from))
                      (at ?p ?to)
                      (not (door ?to ?color))
                      (floor ?to)
                      ;; This is needed to handle the special case of 
                      ;; green keys and doors, but it seems to cause an 
                      ;; assertion error in FD
                      ;;(when (not (= ?color green))
                        ;;(not (has-keys ?color ?okeys))
                        ;;(has-keys ?color ?nkeys))
                      (not (has-keys ?color ?okeys))
                      (has-keys ?color ?nkeys)
                      )
   )
)
