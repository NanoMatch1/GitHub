#include "colors.inc"
#include "finish.inc"

global_settings {assumed_gamma 1 max_trace_level 6}
background {color White transmit 1.0}
camera {orthographic
  right -6.21*x up 6.50*y
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

cylinder {< -1.21,  -1.21,  -3.04>, < -2.37,   0.59,  -1.66>, Rcell pigment {Black}}
cylinder {<  0.12,   0.16,  -1.37>, < -1.04,   1.96,   0.02>, Rcell pigment {Black}}
cylinder {<  0.59,   2.62,  -1.83>, < -0.57,   4.42,  -0.45>, Rcell pigment {Black}}
cylinder {< -0.74,   1.25,  -3.50>, < -1.90,   3.04,  -2.12>, Rcell pigment {Black}}
cylinder {< -1.21,  -1.21,  -3.04>, <  0.12,   0.16,  -1.37>, Rcell pigment {Black}}
cylinder {< -2.37,   0.59,  -1.66>, < -1.04,   1.96,   0.02>, Rcell pigment {Black}}
cylinder {< -1.90,   3.04,  -2.12>, < -0.57,   4.42,  -0.45>, Rcell pigment {Black}}
cylinder {< -0.74,   1.25,  -3.50>, <  0.59,   2.62,  -1.83>, Rcell pigment {Black}}
cylinder {< -1.21,  -1.21,  -3.04>, < -0.74,   1.25,  -3.50>, Rcell pigment {Black}}
cylinder {< -2.37,   0.59,  -1.66>, < -1.90,   3.04,  -2.12>, Rcell pigment {Black}}
cylinder {< -1.04,   1.96,   0.02>, < -0.57,   4.42,  -0.45>, Rcell pigment {Black}}
cylinder {<  0.12,   0.16,  -1.37>, <  0.59,   2.62,  -1.83>, Rcell pigment {Black}}
atom(< -1.21,  -1.21,  -3.04>, 0.76, rgb <0.78, 0.50, 0.20>, 0.0, ase2) // #0
cylinder {< -1.21,  -1.21,  -3.04>, < -0.98,   0.02,  -3.27>, Rbond texture{pigment {color rgb <0.78, 0.50, 0.20> transmit 0.0} finish{ase2}}}
cylinder {< -1.21,  -1.21,  -3.04>, < -1.45,  -2.44,  -2.81>, Rbond texture{pigment {color rgb <0.78, 0.50, 0.20> transmit 0.0} finish{ase2}}}
cylinder {< -1.21,  -1.21,  -3.04>, < -0.78,  -1.75,  -1.97>, Rbond texture{pigment {color rgb <0.78, 0.50, 0.20> transmit 0.0} finish{ase2}}}
cylinder {< -1.21,  -1.21,  -3.04>, < -1.65,  -0.67,  -4.11>, Rbond texture{pigment {color rgb <0.78, 0.50, 0.20> transmit 0.0} finish{ase2}}}
cylinder {< -1.21,  -1.21,  -3.04>, < -0.55,  -0.52,  -2.20>, Rbond texture{pigment {color rgb <0.78, 0.50, 0.20> transmit 0.0} finish{ase2}}}
cylinder {< -1.21,  -1.21,  -3.04>, < -1.88,  -1.90,  -3.88>, Rbond texture{pigment {color rgb <0.78, 0.50, 0.20> transmit 0.0} finish{ase2}}}
cylinder {< -1.21,  -1.21,  -3.04>, < -2.46,  -1.00,  -3.19>, Rbond texture{pigment {color rgb <0.78, 0.50, 0.20> transmit 0.0} finish{ase2}}}
cylinder {< -1.21,  -1.21,  -3.04>, <  0.03,  -1.42,  -2.89>, Rbond texture{pigment {color rgb <0.78, 0.50, 0.20> transmit 0.0} finish{ase2}}}
cylinder {< -1.21,  -1.21,  -3.04>, < -2.03,  -1.54,  -2.12>, Rbond texture{pigment {color rgb <0.78, 0.50, 0.20> transmit 0.0} finish{ase2}}}
cylinder {< -1.21,  -1.21,  -3.04>, < -0.40,  -0.88,  -3.96>, Rbond texture{pigment {color rgb <0.78, 0.50, 0.20> transmit 0.0} finish{ase2}}}
cylinder {< -1.21,  -1.21,  -3.04>, < -1.79,  -0.31,  -2.35>, Rbond texture{pigment {color rgb <0.78, 0.50, 0.20> transmit 0.0} finish{ase2}}}
cylinder {< -1.21,  -1.21,  -3.04>, < -0.63,  -2.11,  -3.73>, Rbond texture{pigment {color rgb <0.78, 0.50, 0.20> transmit 0.0} finish{ase2}}}
// no constraints
