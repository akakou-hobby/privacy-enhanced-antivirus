import syft as sy


def get_cluster():
    server1 = sy.TFEWorker(host='serv0:4000')
    server2 = sy.TFEWorker(host='serv1:4000')
    server3 = sy.TFEWorker(host='serv2:4000')

    cluster = sy.TFECluster(server1, server2, server3)

    return cluster
