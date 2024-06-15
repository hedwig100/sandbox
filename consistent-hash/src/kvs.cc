#include "kv_store.h"
#include <iostream>
#include <string>
#include <utility>

void print_pair(const std::pair<std::string, int> &pair) {
    std::cout << "(" << pair.first << "," << pair.second << ")\n";
}

int main() {
    kvs::DistributedKeyValueStore dkvs(/*default_address*/ "127.0.0.1");
    dkvs.add_node("192.0.0.1");
    dkvs.add_node("192.0.0.2");
    dkvs.add_node("192.0.0.3");
    dkvs.add_node("192.0.0.4");
    dkvs.add_node("192.0.0.5");
    dkvs.add_node("192.0.0.6");
    dkvs.add_node("192.0.0.7");
    dkvs.add_node("192.0.0.8");
    dkvs.add_node("192.0.0.9");
    dkvs.add_node("192.0.0.10");

    dkvs.insert_or_update("01234", 6);
    dkvs.insert_or_update("abcde", 1);
    dkvs.insert_or_update("56789", 2);
    dkvs.insert_or_update("fghij", 3);
    dkvs.insert_or_update("13579", 4);
    dkvs.insert_or_update("klmno", 5);
    dkvs.insert_or_update("aiueo", 7);
    dkvs.insert_or_update("kkkkk", 8);
    dkvs.insert_or_update("sssss", 9);
    dkvs.insert_or_update("italy", 10);
    dkvs.insert_or_update("fender", 11);
    dkvs.insert_or_update("gibson", 12);

    print_pair(dkvs.select("01234"));
    print_pair(dkvs.select("abcde"));
    print_pair(dkvs.select("56789"));
    print_pair(dkvs.select("fghij"));
    print_pair(dkvs.select("13579"));
    print_pair(dkvs.select("klmno"));
    print_pair(dkvs.select("aiueo"));
    print_pair(dkvs.select("kkkkk"));
    print_pair(dkvs.select("sssss"));
    print_pair(dkvs.select("italy"));
    print_pair(dkvs.select("fender"));
    print_pair(dkvs.select("gibson"));

    std::cout << "Remove keys\n";
    dkvs.remove_node("192.0.0.1");
    dkvs.remove_node("192.0.0.3");
    dkvs.remove_node("192.0.0.5");
    dkvs.remove_node("192.0.0.7");
    dkvs.remove_node("192.0.0.9");

    print_pair(dkvs.select("01234"));
    print_pair(dkvs.select("abcde"));
    print_pair(dkvs.select("56789"));
    print_pair(dkvs.select("fghij"));
    print_pair(dkvs.select("13579"));
    print_pair(dkvs.select("klmno"));
    print_pair(dkvs.select("aiueo"));
    print_pair(dkvs.select("kkkkk"));
    print_pair(dkvs.select("sssss"));
    print_pair(dkvs.select("italy"));
    print_pair(dkvs.select("fender"));
    print_pair(dkvs.select("gibson"));
}