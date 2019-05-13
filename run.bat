:start
	python Second.py
	if NOT ERRORLEVEL 1 (
		del codeforces-upsolving1.html
		rename tmp.1.html codeforces-upsolving1.html
		del codeforces-upsolving2.html
		rename tmp.2.html codeforces-upsolving2.html	
		del codeforces-upsolving3.html
		rename tmp.3.html codeforces-upsolving3.html	
		del codeforces-upsolving4.html
		rename tmp.4.html codeforces-upsolving4.html	
rem		del codeforces-upsolving5.html
rem		rename tmp.5.html codeforces-upsolving5.html	
		del codeforces-upsolving6.html
		rename tmp.6.html codeforces-upsolving6.html	
		del codeforces-upsolving7.html
		rename tmp.7.html codeforces-upsolving7.html	
		del codeforces-upsolving8.html
		rename tmp.8.html codeforces-upsolving8.html	
	)
	
rem	ping localhost -n 60 > null
	goto start
	