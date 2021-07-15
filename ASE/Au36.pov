#include "colors.inc"
#include "finish.inc"

global_settings {assumed_gamma 1 max_trace_level 6}
background {color White transmit 1.0}
camera {orthographic
  right -24.08*x up 25.20*y
  direction 1.00*z
  location <0,0,50.00> look_at <0,0,0>}


light_source {<  2.00,   3.00,  40.00> color White
  area_light <0.70, 0, 0>, <0, 0.70, 0>, 3, 3
  adaptive 1 jitter}
// no fog
#declare simple = finish {phong 0.7}
#declare pale = finish {ambient 0.5 diffuse 0.85 roughness 0.001 specular 0.200 }
#declare intermediate = finish {ambient 0.3 diffuse 0.6 specular 0.1 roughness 0.04}
#declare vmd = finish {ambient 0.0 diffuse 0.65 phong 0.1 phong_size 40.0 specular 0.5 }
#declare jmol = finish {ambient 0.2 diffuse 0.6 specular 1 roughness 0.001 metallic}
#declare ase2 = finish {ambient 0.05 brilliance 3 diffuse 0.6 metallic specular 0.7 roughness 0.04 reflection 0.15}
#declare ase3 = finish {ambient 0.15 brilliance 2 diffuse 0.6 metallic specular 1.0 roughness 0.001 reflection 0.0}
#declare glass = finish {ambient 0.05 diffuse 0.3 specular 1.0 roughness 0.001}
#declare glass2 = finish {ambient 0.01 diffuse 0.3 specular 1.0 reflection 0.25 roughness 0.001}
#declare Rcell = 0.070;
#declare Rbond = 0.100;

#macro atom(LOC, R, COL, TRANS, FIN)
  sphere{LOC, R texture{pigment{color COL transmit TRANS} finish{FIN}}}
#end
#macro constrain(LOC, R, COL, TRANS FIN)
union{torus{R, Rcell rotate 45*z texture{pigment{color COL transmit TRANS} finish{FIN}}}
     torus{R, Rcell rotate -45*z texture{pigment{color COL transmit TRANS} finish{FIN}}}
     translate LOC}
#end

cylinder {< -8.05,  -8.05, -10.00>, <  9.26,  -8.05, -10.00>, Rcell pigment {Black}}
cylinder {< -8.05,   9.26, -10.00>, <  9.26,   9.26, -10.00>, Rcell pigment {Black}}
cylinder {< -8.05,   9.26,   0.00>, <  9.26,   9.26,   0.00>, Rcell pigment {Black}}
cylinder {< -8.05,  -8.05,   0.00>, <  9.26,  -8.05,   0.00>, Rcell pigment {Black}}
cylinder {< -8.05,  -8.05, -10.00>, < -8.05,   9.26, -10.00>, Rcell pigment {Black}}
cylinder {<  9.26,  -8.05, -10.00>, <  9.26,   9.26, -10.00>, Rcell pigment {Black}}
cylinder {<  9.26,  -8.05,   0.00>, <  9.26,   9.26,   0.00>, Rcell pigment {Black}}
cylinder {< -8.05,  -8.05,   0.00>, < -8.05,   9.26,   0.00>, Rcell pigment {Black}}
cylinder {< -8.05,  -8.05, -10.00>, < -8.05,  -8.05,   0.00>, Rcell pigment {Black}}
cylinder {<  9.26,  -8.05, -10.00>, <  9.26,  -8.05,   0.00>, Rcell pigment {Black}}
cylinder {<  9.26,   9.26, -10.00>, <  9.26,   9.26,   0.00>, Rcell pigment {Black}}
cylinder {< -8.05,   9.26, -10.00>, < -8.05,   9.26,   0.00>, Rcell pigment {Black}}
atom(< -8.05,  -8.05,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #0
atom(< -5.16,  -8.05,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #1
atom(< -2.28,  -8.05,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #2
atom(<  0.61,  -8.05,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #3
atom(<  3.49,  -8.05,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #4
atom(<  6.38,  -8.05,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #5
atom(< -8.05,  -5.16,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #6
atom(< -5.16,  -5.16,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #7
atom(< -2.28,  -5.16,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #8
atom(<  0.61,  -5.16,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #9
atom(<  3.49,  -5.16,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #10
atom(<  6.38,  -5.16,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #11
atom(< -8.05,  -2.28,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #12
atom(< -5.16,  -2.28,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #13
atom(< -2.28,  -2.28,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #14
atom(<  0.61,  -2.28,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #15
atom(<  3.49,  -2.28,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #16
atom(<  6.38,  -2.28,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #17
atom(< -8.05,   0.61,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #18
atom(< -5.16,   0.61,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #19
atom(< -2.28,   0.61,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #20
atom(<  0.61,   0.61,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #21
atom(<  3.49,   0.61,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #22
atom(<  6.38,   0.61,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #23
atom(< -8.05,   3.49,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #24
atom(< -5.16,   3.49,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #25
atom(< -2.28,   3.49,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #26
atom(<  0.61,   3.49,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #27
atom(<  3.49,   3.49,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #28
atom(<  6.38,   3.49,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #29
atom(< -8.05,   6.38,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #30
atom(< -5.16,   6.38,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #31
atom(< -2.28,   6.38,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #32
atom(<  0.61,   6.38,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #33
atom(<  3.49,   6.38,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #34
atom(<  6.38,   6.38,  -5.00>, 1.21, rgb <1.00, 0.82, 0.13>, 0.0, jmol) // #35

// no constraints
