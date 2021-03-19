# Simple chatting using socket

## Requirement

- python 3^

## How to Run

* pertama jalankan server.py pada terminal

  * python server.py

* kedua jalankan client.py pada terminal

  * python client.py

## Penjelasan App
- import select 
> digunakan untuk memantau banyak koneksi socket
- server menunggu client yang akan masuk
- ketika client masuk, client diminta memasukkan nama 
- semua user disimpan dalam sebuah dictionary clients
- sedangkan semua informasi mengenai ip address dan port 
- disimpan dalam socket_list