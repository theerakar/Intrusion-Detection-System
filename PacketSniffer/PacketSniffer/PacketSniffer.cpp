#include <iostream>
#include <fstream>
#include <pcap.h>
#include <ctime>
#include <string>

#ifdef _MSC_VER
#pragma warning(disable: 4996)
#endif

std::ofstream outputFile;

void packet_handler(u_char* param, const struct pcap_pkthdr* header, const u_char* pkt_data) {
    time_t timestamp_seconds = header->ts.tv_sec;
    struct tm* ltime = localtime(&timestamp_seconds);
    char timestamp_str[32];
    strftime(timestamp_str, sizeof(timestamp_str), "%Y-%m-%d %H:%M:%S", ltime);

    int packet_length = header->len;

    if (outputFile.is_open()) {
        outputFile << timestamp_str << "," << packet_length << std::endl;
        static int packet_count = 0;
        if (++packet_count % 100 == 0) { // Print a message every 100 packets
            std::cout << "Packet captured. " << packet_count << " packets so far." << std::endl;
        }
    }
}

int main() {
    pcap_if_t* alldevs;
    pcap_if_t* d;
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t* adhandle;
    int i = 0;
    int choice;
    std::string output_filename = "packet_data.csv"; // Fixed filename

    if (pcap_findalldevs(&alldevs, errbuf) == -1) {
        std::cerr << "Error in pcap_findalldevs: " << errbuf << std::endl;
        return 1;
    }

    std::cout << "Interfaces found:" << std::endl;
    for (d = alldevs; d; d = d->next) {
        std::cout << ++i << ". " << d->name;
        if (d->description) {
            std::cout << " (" << d->description << ")" << std::endl;
        }
        else {
            std::cout << " (No description available)" << std::endl;
        }
    }

    if (i == 0) {
        std::cout << "No interfaces found!" << std::endl;
        return 2;
    }

    std::cout << "\nEnter the interface number to sniff: ";
    std::cin >> choice;

    if (choice < 1 || choice > i) {
        std::cout << "Interface number out of range." << std::endl;
        pcap_freealldevs(alldevs);
        return 3;
    }

    outputFile.open(output_filename, std::ios::app);
    if (!outputFile.is_open()) {
        std::cerr << "Error opening output file!" << std::endl;
        pcap_freealldevs(alldevs);
        return 5;
    }

    for (d = alldevs, i = 0; i < choice - 1; d = d->next, i++);
    adhandle = pcap_open_live(d->name, 65536, 1, 1000, errbuf);

    if (adhandle == nullptr) {
        std::cerr << "Unable to open adapter " << d->name << ": " << errbuf << std::endl;
        pcap_freealldevs(alldevs);
        outputFile.close();
        return 4;
    }

    std::cout << "\nListening on " << d->description << "... Press Ctrl+C to stop." << std::endl;

    pcap_loop(adhandle, 0, packet_handler, nullptr);

    pcap_close(adhandle);
    pcap_freealldevs(alldevs);
    outputFile.close();

    return 0;
}