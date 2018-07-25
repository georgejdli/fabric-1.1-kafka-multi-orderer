import string
from sys import argv

script, arg1 = argv
arg1 = int(arg1)

for i in range(arg1):
    file = """version: '2'

services:
  ca.org1.example.com:
    image: hyperledger/fabric-ca:$ARCH-1.1.0
    environment:
      - FABRIC_CA_HOME=/etc/hyperledger/fabric-ca-server
      - FABRIC_CA_SERVER_CA_NAME=ca.org1.example.com
      - FABRIC_CA_SERVER_TLS_ENABLED=true
      - FABRIC_CA_SERVER_TLS_CERTFILE=/etc/hyperledger/fabric-ca-server-config/ca.org1.example.com-cert.pem
      - FABRIC_CA_SERVER_TLS_KEYFILE=/etc/hyperledger/fabric-ca-server-config/{ORG1-CA-KEY}

    ports:
      - "7054:7054"
    command: sh -c 'fabric-ca-server start --ca.certfile /etc/hyperledger/fabric-ca-server-config/ca.org1.example.com-cert.pem --ca.keyfile /etc/hyperledger/fabric-ca-server-config/{ORG1-CA-KEY} -b admin:adminpw -d'
    volumes:
      - ./crypto-config/peerOrganizations/org1.example.com/ca/:/etc/hyperledger/fabric-ca-server-config
    container_name: ca.org1.example.com

  zookeeper0:
    container_name: zookeeper0
  # image: tmeister/zookeeper:latest
    image: hyperledger/fabric-zookeeper:$ARCH-0.4.6
    restart: always
    environment:
      - ZOO_MY_ID=1
      - ZOO_SERVERS=server.1=zookeeper0:2888:3888 server.2=zookeeper1:2888:3888 server.3=zookeeper2:2888:3888
    ports:  
      - 2181:2181
      - '2888'
      - '3888'

  zookeeper1:
    container_name: zookeeper1
  # image: tmeister/zookeeper:latest
    image: hyperledger/fabric-zookeeper:$ARCH-0.4.6
    restart: always
    environment:
      - ZOO_MY_ID=2
      - ZOO_SERVERS=server.1=zookeeper0:2888:3888 server.2=zookeeper1:2888:3888 server.3=zookeeper2:2888:3888
    ports:  
      - 3181:2181
      - '2888'
      - '3888'

  zookeeper2:
    container_name: zookeeper2
  # image: tmeister/zookeeper:latest
    image: hyperledger/fabric-zookeeper:$ARCH-0.4.6
    restart: always
    environment:
      - ZOO_MY_ID=3
      - ZOO_SERVERS=server.1=zookeeper0:2888:3888 server.2=zookeeper1:2888:3888 server.3=zookeeper2:2888:3888
    ports:  
      - 4181:2181
      - '2888'
      - '3888'

  root.org1.example.com:
    container_name: root.org1.example.com
    image: hyperledger/fabric-peer:$ARCH-1.1.0
    environment:
      - CORE_LOGGING_PEER=debug
      - CORE_CHAINCODE_LOGGING_LEVEL=DEBUG
      - CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock
      - CORE_PEER_ID=root.org1.example.com
      - CORE_PEER_ADDRESS=root.org1.example.com:7051
      - CORE_VM_DOCKER_HOSTCONFIG_NETWORKMODE=composer_default
      - CORE_PEER_LOCALMSPID=Org1MSP
      - CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/peer/msp
      - CORE_LEDGER_STATE_STATEDATABASE=CouchDB
      - CORE_LEDGER_STATE_COUCHDBCONFIG_COUCHDBADDRESS=couchdb:5984
      - CORE_PEER_GOSSIP_EXTERNALENDPOINT=root.org1.example.com:7051
      - CORE_PEER_GOSSIP_BOOTSTRAP=root.org1.example.com:7051
      - CORE_PEER_TLS_ENABLED=true
      - CORE_PEER_GOSSIP_USELEADERELECTION=true
      - CORE_PEER_GOSSIP_ORGLEADER=false
      - CORE_PEER_PROFILE_ENABLED=true
      - CORE_PEER_TLS_CERT_FILE=/etc/hyperledger/peer/tls/server.crt
      - CORE_PEER_TLS_KEY_FILE=/etc/hyperledger/peer/tls/server.key
      - CORE_PEER_TLS_ROOTCERT_FILE=/etc/hyperledger/peer/tls/ca.crt
    working_dir: /opt/gopath/src/github.com/hyperledger/fabric
    command: peer node start
    ports:
      - 7051:7051
      - 7053:7053
    volumes:
        - /var/run/:/host/var/run/
        - ./:/etc/hyperledger/configtx
        - ./crypto-config/peerOrganizations/org1.example.com/peers/root.org1.example.com/msp:/etc/hyperledger/peer/msp
        - ./crypto-config/peerOrganizations/org1.example.com/peers/root.org1.example.com/tls:/etc/hyperledger/peer/tls
        - ./crypto-config/peerOrganizations/org1.example.com/users:/etc/hyperledger/msp/users
        - ./crypto-config/ordererOrganizations/example.com/orderers/orderer0.example.com/msp:/etc/hyperledger/msp/orderer/msp
"""