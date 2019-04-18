:start
	python Second.py
	if NOT ERRORLEVEL 1 (
		del codeforces-upsolving1.html
		rename tmp.1.html codeforces-upsolving1.html
		del codeforces-upsolving2.html
		rename tmp.2.html codeforces-upsolving2.html	
		del codeforces-upsolving3.html
		rename tmp.3.html codeforces-upsolving3.html	
rem		del codeforces-upsolving4.html
rem		rename tmp.4.html codeforces-upsolving4.html	
rem		del codeforces-upsolving5.html
rem		rename tmp.5.html codeforces-upsolving5.html	
rem		del tmp.6.html
rem		del codeforces-upsolving7.html
rem		rename tmp.7.html codeforces-upsolving7.html	
	)
	
	ping localhost -n 60 > null
	goto start
	