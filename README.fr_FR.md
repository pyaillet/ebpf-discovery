# Découverte d'eBPF

En tant qu'utilisateur de Linux, il est possible que la seule chose qui vous
intéresse soit l'inclusion de la dernière version des drivers de votre matériel
dans le noyau.
Pourtant, c'est loin d'être le seul pan du kernel qui évolue !
Ce sont notamment des évolutions du kernel (namespace, cgroups, ...) qui ont
permis de développer les conteneurs logiciels tels que Docker.
Dans cet article, je vous propose de découvrir une autre innovation majeure du
kernel : eBPF (ce n'est pas moi qui le dit mais [The New Stack](https://thenewstack.io/linux-technology-for-the-new-year-ebpf/)).

## Historique

Historiquement, lorsqu'on souhaitait faire de la capture réseau sous Unix,
cette opération était réalisée dans l'espace utilisateur (c'est à dire en
dehors du kernel).
En général, lorsqu'on souhaite capturer du traffic réseau pour identifier un
problème, on ne veut pas l'ensemble du traffic mais on souhaite filtrer selon
certains critères (protocole, destination, ...).
Pourtant en pratique, cela nécessitait de copier l'intégralité des paquets
depuis le kernel vers l'espace utilisateur avant même de déterminer si un
paquet était intéressant à conserver pour une session particulière de capture.

Ainsi en 1992, Steve McCanne et Van Jacobson ont publié
[un article](http://www.tcpdump.org/papers/bpf-usenix93.pdf) proposant une
nouvelle architecture pour la capture de paquets en espace utilisateur.
Celle-ci repose sur une machine virtuelle à registres qui fonctionne dans le
kernel et permet d'évaluer les règles de filtrage des paquets sans recopie des
paquets.
Ce mécanisme a été intégré au noyau Linux
[en 1997 dans la version 2.1.75](https://lwn.net/1998/0212/).
Il est disponible sur la plupart des Unix et est utilisée par des outils
standards comme [tcpdump](https://www.tcpdump.org/) pour sélectionner les
paquets à capturer.
À ce moment là, la machine virtuelle BPF est assez limitée : elle ne comporte
que 2 registres 32 bits, une pile de taille minimaliste et ne supporte que les
sauts vers l'avant.

En 2012, une [évolution de bpf](https://lwn.net/Articles/475043/) est proposée
afin de sécuriser et filtrer certains appels systèmes en attachant à leur appel
un programme bpf permettant d'évaluer le contexte et de permettre ou interdire
l'appel comme cela était fait pour le traitement du traffic réseau.

Mais l'évolution majeure arrive en 2013, Alexei Starovoitov propose alors
[Extended BPF](https://lwn.net/Articles/575531/). Voici un résumé de ces
évolutions :

- Un vérifieur qui s'assure que le code est sûr :
  - pas de boucles infinies
  - pas d'utilisation de pointeurs non vérifiés
  - ...
- Un compilateur JIT pour transformer le programme BPF en code natif
- L'extension des capacités de la machine virtuelle :
  - passage de 2 registres 32 bits à 10 registres 64 bits
  - possibilité d'appeler certaines fonctions du kernel

Par la suite, d'autres fonctionnalités seront encore intégrées :

- utilisation de [maps](https://prototype-kernel.readthedocs.io/en/latest/bpf/ebpf_maps.html) pour l'échange d'information entre le programme bpf et l'espace utilisateur
- la possibilité d'instrumenter encore plus d'événements du kernel avec des programmes bpf
- ...

Pour une liste complète, n'hésitez pas à vous référer à
[la page de Brendan Gregg](http://www.brendangregg.com/ebpf.html) sur le sujet.
En particulier, ce [schéma](http://www.brendangregg.com/eBPF/linux_ebpf_support.png).

Pour résumer, BPF est l'appellation d'origine. Linux a introduit l'appellation
eBPF et pour différencier de l'ancienne version celle-ci est parfois nommée
cBPF.
Donc :

- lorsqu'on vous parle de cBPF c'est sans les extensions
- lorsqu'on vous parle d'eBPF il s'agit de la version moderne
- lorsqu'on vous parle de BPF `¯\_(ツ)_/¯`

## Principe

Maintenant, qu'on en connaît un peu plus sur l'historique du projet, voyons
comment il fonctionne...

### Fonctionnement

Tout est basé sur un appel système :

```c
#include <linux/bpf.h>

int bpf(int cmd, union bpf_attr *attr, unsigned int size);
```

Le premier argument `cmd` indique l'action à réaliser, exemple : `BPF_PROG_LOAD`, pour charger un programme bpf.
Le deuxième argument `attr` porte les paramètres de l'action à réaliser, sa structure dépend de la commande (valeur du premier argument).
Le dernier paramètre `size` est la taille de la structure passée en deuxième
argument.

Afin d'échanger des informations entre le programme BPF qui tourne dans
l'espace du noyau et l'espace utilisateur. eBPF propose de créer et de
manipuler des maps. Les autres commandes utilisables avec BPF sont dédiées à la
manipulation de ces maps.

- Détail sur BPF_LOAD
  - prog type
  - prog content (utilisation de LLVM)

- Machine virtuelle sandboxée
- Jeu d'instruction
- JIT
- Verifier

### BCC : BPF Compiler Collection

Tout cela peut sembler un peu compliqué à mettre en oeuvre. Heureusement, il
existe

Tracing events: /sys/kernel/debug/tracing/available_events

## Cas d'utilisation

La technologie eBPF est en plein essor, le fait de pouvoir exécuter du code en
mode kernel intéresse beaucoup, d'autant plus qu'avec eBPF, il n'est pas
nécessaire de recompiler le noyau ou d'être spécialiste du développement de
modules pour pouvoir le faire.
Ainsi, le projet est utilisé pour :

- De la capture d'événements du kernel, pour
  - des mesures de performance
  - du tracing
- Du filtrage réseau :
  - haute-performance (anti-DDOS, ...)
  - avancé et dépendant du contexte

## Conclusion

J'espère que ce petit tour d'horizon vous a donné envie d'aller plus loin.
Si c'est le cas, n'hésitez pas à consulter les références que j'ai consultées
pour le rédiger.
Dans un prochain article nous aborderons [Cilium](https://cilium.io/) qui
utilise cette technologie pour proposer une solution réseau multi-facette dans
le contexte des conteneurs et notamment Kubernetes.

## Références

- Historique :
  - Papier original par Steven McCanne et Van Jacobson : http://www.tcpdump.org/papers/bpf-usenix93.pdf 
    et https://www.usenix.org/legacy/publications/library/proceedings/sd93/mccanne.pdf
  - BPF - in-kernel virtual machine : http://vger.kernel.org/netconf2015Starovoitov-bpf_collabsummit_2015feb20.pdf

- Articles :
  - What can BPF do for you ? : https://events.static.linuxfound.org/sites/events/files/slides/iovisor-lc-bof-2016.pdf
  - Awesome eBPF : https://github.com/zoidbergwill/awesome-ebpf
  - How I ended up writing eBPF : https://bolinfest.github.io/opensnoop-native
  - eBPF, past, present and future : https://ferrisellis.com/content/ebpf_past_present_future/
  - eBPF, syscalls and map types : https://ferrisellis.com/content/ebpf_syscall_and_maps/

- Actualité :
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
  - Facebook : http://vger.kernel.org/lpc_net2018_talks/ebpf-firewall-LPC.pdf
  - Cilium : https://cilium.io/
  - Calico : https://www.projectcalico.org/tigera-adds-ebpf-support-to-calico/
  - Tcpdump : https://medium.com/@cjoudrey/capturing-http-packets-the-hard-way-b9c799bfb6
  - Toward a faster Iptables in eBPF : https://webthesis.biblio.polito.it/8475/1/tesi.pdf
  - Toward an eBPF-based clone of iptables : 
    - Slides : https://www.astrid-project.eu/images/Toward%20an%20eBPF-based%20clone%20of%20iptables.pdf
    - Article complet : https://sebymiano.github.io/documents/21-Securing_Linux_with_a_Faster_and_Scalable_Iptables.pdf
