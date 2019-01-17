#!/usr/bin/env python3
from CloudFlare import *
from pprint import pprint
from settings import *
import sys


class IpFetecher(object):
    def get(self):
        pass


class ArgvIpFetecher(object):
    def get(self):
        return sys.argv[1]


class DnsClient(object):
    def __init__(self, credential):
        self.credential = credential

    def get_records(self, type=None, name=None, content=None, **kwargs):
        raise NotImplementedError

    def create_record(self, type, name, content, **kwargs):
        raise NotImplementedError

    def update_record(self, type, name, content, record_id, **kwargs):
        raise NotImplementedError

    def delete_record(self, record_id, **kwargs):
        raise NotImplementedError

    def is_exist(self, type, name, content=None, **kwargs):
        return len(self.get_records(type, name, content, **kwargs)) == 0


class CloudflareClient(DnsClient):
    def __init__(self, credential):
        super().__init__(credential)
        self.client = CloudFlare(**self.credential['api_key'])
        self.zone_id = self.credential['zone_id']
        self.domain_name = self.credential['domain_name']

    def get_records(self, type=None, name=None, content=None, **kwargs):
        return self.client.zones.dns_records.get(
            self.zone_id,
            params={
                'type': type, 'name': name, 'content': content,
                **kwargs
            }
        )

    def create_record(self, type, name, content, **kwargs):
        return self.client.zones.dns_records.post(
            self.zone_id,
            data={
                'type': type, 'name': name, 'content': content,
                **kwargs
            }
        )

    def update_record(self, type, name, content, record_id, **kwargs):
        return self.client.zones.dns_records.put(
            self.zone_id,
            record_id,
            data={
                'type': type, 'name': name, 'content': content,
                **kwargs
            }
        )

    def delete_record(self, record_id, **kwargs):
        return self.client.zones.dns_records.delete(
            self.zone_id,
            record_id,
        )


class DDNSManager(object):
    def __init__(self, client, target_host, ipfetecher):
        self.client = client
        self.target_host = target_host
        self.fetecher = ipfetecher

    def update(self, **kwargs):
        current = self.client.get_records('A', self.target_host)
        try:
            myip = self.fetecher.get()
        except Exception as e:
            print("Fetcher failed, exception <{}>, msg <{}>".format(type(e), e))
            return
        if len(current):
            pprint(self.client.update_record('A', self.target_host, myip, current[0]['id'], **kwargs))
        else:
            pprint(self.client.create_record('A', self.target_host, myip, **kwargs))


def load_config():
    vendor = DNS_VENDOR
    credential = globals()[vendor.upper() + '_CREDENTIAL']
    client = globals()[vendor + 'Client'](credential)
    return DDNSManager(client, TARGET_HOST, globals()[FETCHER]())


if __name__ == '__main__':
    mgr = load_config()
    mgr.update(proxied=False)
