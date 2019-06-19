# Découverte d'eBPF

En tant qu'utilisateur de Linux, il est possible que la seule chose qui vous 
intéresse soit l'inclusion de la dernière version des drivers de votre matériel
dans le noyau.
Pourtant, c'est loin d'être le seul pan du kernel qui évolue !
Ce sont notamment des évolutions du kernel (namespace, cgroups, ...) qui ont
permis de développer les conteneurs logiciels tels que Docker.
Dans cet article, je vous propose de découvrir une autre innovation majeure du
kernel : eBPF (ce n'est pas moi qui le dit mais [The New Stack](lien)).

## Historique

- BPF introduit par deux articles de 1992 et 1993
  - Objectif capture de paquets en userspace avec langage de capture
- Linux 3.18 : extended BPF Virtual Machine:
  - 

Pour résumer, BPF est l'appellation d'origine. Linux a introduit l'appellation 
eBPF et pour différencier de l'ancienne version celle-ci est parfois nommée
cBPF.
Donc : 
- lorsqu'on vous parle de cBPF c'est sans les extensions
- lorsqu'on vous parle d'eBPF il s'agit de la version moderne
- lorsqu'on vous parle de BPF `¯\_(ツ)_/¯`

## Principe

- Machine virtuelle sandboxée
- Jeu d'instruction
- JIT
- Verifier

## Utilisation

- bcc


## Conclusion

J'espère que ce petit tour d'horizon vous a donné envie d'aller plus loin.
Dans un prochain article nous détaillerons un cas d'utilisation plus précis
avec la découverte de [Cilium](https://cilium.io/)

## Références

### Outils de tracing

- Strace : https://blog.packagecloud.io/eng/2016/02/29/how-does-strace-work/
- Ptrace : https://medium.com/@lizrice/a-debugger-from-scratch-part-1-7f55417bc85f
- Ltrace : https://www.go4expert.com/articles/ltrace-linux-debugging-utility-tutorial-t29095/

### eBPF : 

- Historique :
  - Papiers originaux par Steven McCanne et Van Jacobson : http://www.tcpdump.org/papers/bpf-usenix93.pdf 
    et https://www.usenix.org/legacy/publications/library/proceedings/sd93/mccanne.pdf

- Acualité :
  - https://thenewstack.io/linux-technology-for-the-new-year-ebpf/

- Documentation :
  - https://en.wikipedia.org/wiki/Berkeley_Packet_Filter
  - Documentation officielle BPF : https://www.kernel.org/doc/html/latest/bpf/index.html
  - BPF and XDP Reference Guide : https://cilium.readthedocs.io/en/latest/bpf/
  - Verifier : https://blogs.oracle.com/linux/notes-on-bpf-5

- Tracing :
  - http://www.linuxembedded.fr/2019/03/les-secrets-du-traceur-ebpf/
  - Java Flame graphs : https://www.youtube.com/watch?v=saCGp-T6saQ
  - Jérémie Lagarde DevoxxFr : https://www.youtube.com/watch?v=rdrnHrQGQlw
  - Liz Rice : https://www.youtube.com/watch?v=4SiWL5tULnQ

- Network :
  - XDP : Netronome - https://github.com/Netronome/bpf-samples
  - Cloudflare : https://blog.cloudflare.com/epbf_sockets_hop_distance/
  - Cilium : https://cilium.io/
  - Calico : https://www.projectcalico.org/tigera-adds-ebpf-support-to-calico/
  - Tcpdump : https://medium.com/@cjoudrey/capturing-http-packets-the-hard-way-b9c799bfb6
  - Toward an eBPF-based clone of iptables : 
    - Slides : https://www.astrid-project.eu/images/Toward%20an%20eBPF-based%20clone%20of%20iptables.pdf
    - Article complet : https://sebymiano.github.io/documents/21-Securing_Linux_with_a_Faster_and_Scalable_Iptables.pdf
    

