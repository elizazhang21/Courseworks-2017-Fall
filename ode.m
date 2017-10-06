solinit=bvpinit(linspace(0,pi,10),[1,1],lmb);
opts=bvpset('Stats','on');
sol=bvp4c(@ODEfun,@BCfun,solinit,opts);
lambda=sol.parameter
x=[0:pi/60:pi];
y=deval(sol,x);
plot(x,y(1:),'b-',sol.x,sol.y(1,:),'ro')
legend('???','??????')
%??ODEfun??
function dydx=ODEfun(x,y,lmb)
q=15;
dydx=[y(2);-(lmb-2*q*cos(2*x))*y(1)];
%??BCfun??
function bc=BCfun(ya,yb,lmb)
bc=[ya(1)-1;ya(2);yb(2)];