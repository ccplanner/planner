;; defineing chips challenge domain

(define (domain chips-challenge)
  (:requirements :equality :typing )
  ;; These additional requirements may be necessary
  ;;(:requirements :equality :typing :adl :derived-predicates)
  (:types type thing location direction number color - object)
  (:predicates (floor ?l - location)
               (at ?l - location)
               (chip ?l - location)
               (socket ?l - location)
               (wall ?l - location)
               (block ?l - location)
               (bomb ?l - location)
               (dirt ?l - location)
               (gravel ?l - location)
               (has-keys ?c - color ?n - number)
               (key ?l - location ?c - color)
               (door ?l - location ?c - color)
               (has-boots ?t - type)
               (boots ?l - location ?t - type)
               (force-floor ?l - location)
               (slide-dir ?l - location ?d - direction)
               (ice ?l - location)
               (ice-wall ?l - location)
               (ice-wall-dir ?l - location ?in - direction ?out - direction)
               (switch-wall-open ?l - location)
               (switch-wall-closed ?l - location)
               (switched-walls-open ?x - number )
               (successor ?n1 - number ?n0 - number)
               (chips-left ?n - number)
               (MOVE-DIR ?from ?to - location ?dir - direction))

  (:action move-floor
   :parameters (?from ?to - location ?dir - direction)
   :precondition (and (at ?from)
                      (floor ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (not (chip-state slipping))
                      (not (chip-state sliding))
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      )
   )
   
  (:action move-dirt
   :parameters (?from ?to - location ?dir - direction)
   :precondition (and (at ?from)
                      (dirt ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (not (chip-state slipping))
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (not (dirt ?to))
                      (floor ?to)
                      )
   )
   
  (:action push-block
   :parameters (?from ?to - location ?dir - direction ?blockto - location)
   :precondition (and (at ?from)
                      (block ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (MOVE-DIR ?to ?blockto ?dir)
                      (not (chip-state slipping)) ;does this matter?
                      (floor ?blockto)
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (not (block ?to))
                      (block ?blockto)
                      (floor ?to)
                      (not (floor ?blockto))
                      )
   )
   
  (:action push-block-into-water
   :parameters (?from ?to - location ?dir - direction ?blockto - location)
   :precondition (and (at ?from)
                      (block ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (MOVE-DIR ?to ?blockto ?dir)
                      (not (chip-state slipping)) ;does this matter?
                      (water ?blockto)
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (not (block ?to))
                      (dirt ?blockto)
                      (floor ?to)
                      (not (water ?blockto))
                      )
   )
   
   ;;these may be uinified into a single action?
  (:action push-block-into-bomb
   :parameters (?from ?to - location ?dir - direction ?blockto - location)
   :precondition (and (at ?from)
                      (block ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (MOVE-DIR ?to ?blockto ?dir)
                      (not (chip-state slipping)) ;does this matter?
                      (bomb ?blockto)
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (not (block ?to))
                      (floor ?blockto)
                      (floor ?to)
                      (not (bomb ?blockto))
                      )
   )
  
  (:action move-socket
   :parameters (?from ?to - location ?dir - direction)
   :precondition (and (at ?from)
                      (socket ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (chips-left n0)
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (not (socket ?to))
                      (floor ?to)
                      )
   )

;; Slide/Force Floors
  (:action move-force
   :parameters (?from ?to - location ?dir - direction)
   :precondition (and (at ?from)
                      (force-floor ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (not (chip-state sliding))
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (chip-state sliding)
                      )
   )

  (:action slide-force-force
   :parameters (?from ?to - location ?dir - direction)
   :precondition (and (at ?from)
                      (force-floor ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (slide-dir ?from ?dir)
                      (chip-state sliding) ;; maybe redundent
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (have-free-move)
                      )
   )

  (:action slide-force-free
   :parameters (?from ?to - location ?dir - direction)
   :precondition (and (at ?from)
                      (force-floor ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (have-free-move)
                      (not (slide-dir ?from ?dir)) ;; if free move then don't go this way
                      (chip-state sliding) ;; maybe redundent
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (not (have-free-move))
                      )
   )

  (:action slide-floor
   :parameters (?from ?to - location ?dir - direction)
   :precondition (and (at ?from)
                      (floor ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (or (slide-dir ?from ?dir) ;; sliding in this dir or use 
                       ;; have-free move
                       (have-free-move))
                      (chip-state sliding) ;; maybe redundent
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (not (chip-state sliding))
                      (not (have-free-move))
                      )
   )

  (:action slide-force-chip
   :parameters (?from ?to - location ?dir - direction ?ochips ?nchips - number)
   :precondition (and (at ?from)
                      (force-floor ?from)
                      (MOVE-DIR ?from ?to ?dir)
                      (or (slide-dir ?from ?dir) ;; sliding in this dir or use 
                       ;; have-free move
                       (have-free-move))
                      (chip-state sliding) ;; maybe redundent
                      (chip ?to) ;;chips stuff
                      (chips-left ?ochips)
                      (or (successor ?nchips ?ochips)
                          ;; handle having n0 chips
                          (and (= ?ochips ?nchips) (= ?ochips n0))
                          )
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (not (have-free-move))
                      (not (chip ?to))
                      (floor ?to)
                      (not (chips-left ?ochips))
                      (chips-left ?nchips)
                      (not (chip-state sliding))
                      )
   )


;; Ice
  (:action move-ice
   :parameters (?from ?to - location ?dir - direction)
   :precondition (and (at ?from)
                      (or (ice ?to) (ice-wall ?to))
                      (MOVE-DIR ?from ?to ?dir)
                      (not (chip-state slipping))
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (chip-state slipping)
                      (slipping-dir ?dir)
                      )
   )

  (:action slip-ice-ice
   :parameters (?from ?to - location ?dir - direction)
   :precondition (and (at ?from)
                      (ice ?from)
                      (or (ice ?to) (ice-wall ?to))
                      (chip-state slipping)
                      (MOVE-DIR ?from ?to ?dir)
                      (slipping-dir ?dir)
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      )
   )

  (:action slip-ice-socket
   :parameters (?from ?to - location ?dir - direction)
   :precondition (and (at ?from)
                      (ice ?from)
                      (or (ice ?to) (ice-wall ?to))
                      (chip-state slipping)
                      (MOVE-DIR ?from ?to ?dir)
                      (slipping-dir ?dir)
                      (chips-left n0)
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (not (socket ?to))
                      (floor ?to)
                      )
   )

  (:action slip-ice-wall-ice
   :parameters (?from ?to - location ?odir - direction ?ndir - direction)
   :precondition (and (at ?from)
                      (ice-wall ?from)
                      (or (ice ?to) (ice-wall ?to))
                      (chip-state slipping)
                      (MOVE-DIR ?from ?to ?ndir)
                      (slipping-dir ?odir)
                      (ice-wall-dir ?from ?odir ?ndir)
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (not (slipping-dir ?odir))
                      (slipping-dir ?ndir)
                      )
   )

  (:action slip-ice-wall-floor
   :parameters (?from ?to - location ?odir - direction ?ndir - direction)
   :precondition (and (at ?from)
                      (ice-wall ?from)
                      (floor ?to)
                      (chip-state slipping)
                      (MOVE-DIR ?from ?to ?ndir)
                      (slipping-dir ?odir)
                      (ice-wall-dir ?from ?odir ?ndir)
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (not (slipping-dir ?odir))
                      (not (chip-state slipping))
                      )
   )

  (:action slip-ice-floor
   :parameters (?from ?to - location ?dir - direction)
   :precondition (and (at ?from)
                      (floor ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (chip-state slipping)
                      (slipping-dir ?dir)
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (not (slipping-dir ?dir))
                      (not (chip-state slipping))
                      )
   )

  (:action slip-ice-wall-chip
   :parameters (?from ?to - location ?odir - direction ?ndir - direction ?ochips ?nchips - number)
   :precondition (and (at ?from)
                      (ice-wall ?from)
                      (chip ?to)
                      (chips-left ?ochips)
                      (or (successor ?nchips ?ochips)
                          ;; handle having n0 chips
                          (and (= ?ochips ?nchips) (= ?ochips n0))
                          )
                      (chip-state slipping)
                      (MOVE-DIR ?from ?to ?ndir)
                      (slipping-dir ?odir)
                      (ice-wall-dir ?from ?odir ?ndir)
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (not (chip ?to))
                      (floor ?to)
                      (not (chips-left ?ochips))
                      (chips-left ?nchips)
                      (not (slipping-dir ?odir))
                      (not (chip-state slipping))
                      )
   )

  (:action slip-ice-chip
   :parameters (?from ?to - location ?dir - direction ?ochips ?nchips - number)
   :precondition (and (at ?from)
                      (chip ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (chips-left ?ochips)
                      (or (successor ?nchips ?ochips)
                          ;; handle having n0 chips
                          (and (= ?ochips ?nchips) (= ?ochips n0))
                          )
                      (chip-state slipping)
                      (slipping-dir ?dir)
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
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
   :parameters (?from ?to - location ?dir - direction)
   :precondition (and (at ?from)
                      (switch-wall-open ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (switched-walls-open n0)
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      )
   )

  (:action move-switch-wall-closed
   :parameters (?from ?to - location ?dir - direction)
   :precondition (and (at ?from)
                      (switch-wall-closed ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (not (switched-walls-open n0))
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      )
   )

  (:action move-toggle-walls-open
   :parameters (?from ?to - location ?dir - direction)
   :precondition (and (at ?from)
                      (green-button ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (not (switched-walls-open n0))
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (switched-walls-open n0)
                      )
   )

  (:action move-toggle-walls-closed
   :parameters (?from ?to - location ?dir - direction)
   :precondition (and (at ?from)
                      (green-button ?to)
                      (MOVE-DIR ?from ?to ?dir)
                      (switched-walls-open n0)
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (not (switched-walls-open n0))
                      )
  )
   
;; maybe make zero a succesor to itself
  (:action move-chip
   :parameters (?from ?to - location ?dir - direction ?ochips ?nchips - number)
   :precondition (and (at ?from)
                      (chip ?to)
                      (not (chip-state sliding))
                      (not (chip-state slipping))
                      (MOVE-DIR ?from ?to ?dir)
                      (chips-left ?ochips)
                      (or (successor ?nchips ?ochips)
                          ;; handle having n0 chips
                          (and (= ?ochips ?nchips) (= ?ochips n0))
                          )
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (not (chip ?to))
                      (floor ?to)
                      (not (chips-left ?ochips))
                      (chips-left ?nchips)
                      )
   )

;; Keys

;; Move to a tile containing a ?color key, having had ?okeys ?color keys already.
;; TODO Need to increase 'successor' numbers to accomodate large numbers of keys?
  (:action move-key
   :parameters (?from ?to - location ?dir - direction ?color - color ?okeys ?nkeys - number)
   :precondition (and (at ?from)
                      (key ?to ?color)
                      (MOVE-DIR ?from ?to ?dir)
                      (has-keys ?color ?okeys)
                      (successor ?okeys ?nkeys)
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (not (key ?to ?color))
                      (floor ?to)
                      (not (has-keys ?color ?okeys))
                      (has-keys ?color ?nkeys)
                      )
   )

;; Move to a tile containing a ?color door, having ?okeys ?color keys already.
;; Need to indicate to the planner special :requirement to handle 
;; the '=' or 'when' such as 'adl?  See 'benchmarks/psr-large/domain.pddl'?
;; It seems not.
;; Should colors be 'constants' instead of 'objects'?  Seems to work the way it is.
  (:action move-door
   :parameters (?from ?to - location ?dir - direction ?color - color ?okeys ?nkeys - number)
   :precondition (and (at ?from)
                      (door ?to ?color)
                      (MOVE-DIR ?from ?to ?dir)
                      (has-keys ?color ?okeys)
                      (successor ?nkeys ?okeys)
                      (not (has-keys ?color n0))
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (not (door ?to ?color))
                      (floor ?to)
                      (when (not (= ?color green))
                        (and 
                          (not (has-keys ?color ?okeys))
                          (has-keys ?color ?nkeys))
                        )
                      )
   )


  (:action move-boots
   :parameters (?from ?to - location ?dir - direction ?t - type)
   :precondition (and (at ?from)
                      (boots ?to ?t)
                      (not (has-boots ?t))
                      (MOVE-DIR ?from ?to ?dir)
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      (not (boots ?to ?t))
                      (floor ?to)
                      (has-boots ?t)
                      )
   )

  (:action walk-on-water
   :parameters (?from ?to - location ?dir - direction)
   :precondition (and (at ?from)
                      (water ?to)
                      (has-boots water)
                      (MOVE-DIR ?from ?to ?dir)
                      (not (chip-state slipping))
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      )
   )

  (:action walk-on-fire
   :parameters (?from ?to - location ?dir - direction)
   :precondition (and (at ?from)
                      (fire ?to)
                      (has-boots fire)
                      (MOVE-DIR ?from ?to ?dir)
                      (not (chip-state slipping))
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      )
   )

  (:action walk-on-ice
   :parameters (?from ?to - location ?dir - direction)
   :precondition (and (at ?from)
                      (ice ?to)
                      (has-boots ice)
                      (MOVE-DIR ?from ?to ?dir)
                      (not (chip-state slipping))
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      )
   )

  (:action walk-on-force-floor
   :parameters (?from ?to - location ?dir - direction)
   :precondition (and (at ?from)
                      (force-floor ?to)
                      (has-boots slide)
                      (MOVE-DIR ?from ?to ?dir)
                      )
   :effect       (and (not (at ?from))
                      (at ?to)
                      )
   )
)
