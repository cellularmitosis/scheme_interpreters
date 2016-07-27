(define (not x) (if x False True))
(define (>= x y) (or (> x y) (= x y)))
(define (<= x y) (or (< x y) (= x y)))
