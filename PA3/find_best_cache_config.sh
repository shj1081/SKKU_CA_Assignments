#!/bin/bash

# Define the array of cache configurations
declare -a cache_configs=("1:256:64" "2:128:64" "4:64:64" "8:32:64" "16:16:64" "32:8:64" "64:4:64" "128:2:64" "256:1:64")

# Define the array of applications
declare -a apps=("CCa" "CCe" "CCh" "CCh_st" "CCl" "CCm" "CF1" "CRd" "CRf" "CRm" "CS1" "CS3" "DP1d" "DP1f" "DPcvt" "DPT" "DPTd" "ED1" "EF" "EI" "EM1" "EM5" "M_Dyn" "MC" "MCS" "MD" "MI" "MIM" "MIM2" "MIP" "ML2" "ML2_BW_ld" "ML2_BW_ldst" "ML2_BW_st" "ML2_st" "MM" "MM_st" "STc" "STL2" "STL2b")

# Initialize an associative array to store the best configuration for each app
declare -A best_configs

# Initialize an associative array to store the best miss rate for each app
declare -A best_miss_rates

# Loop over each cache configuration
for config in "${cache_configs[@]}"; do
    # Loop over each application
    for app in "${apps[@]}"; do
        # Run the Spike simulator
        output=$(./spike --dc=$config ~swe3005/2023f/proj3/pk ~swe3005/2023f/proj3/bench/${app}.elf)

        # Extract the last line and get the miss rate
        miss_rate=$(echo "$output" | grep 'D\$ Miss Rate:' | awk '{print $4}' | tr -d '%')

        # Check if this is the best miss rate for this app
        if [ -z "${best_miss_rates[$app]}" ] || [ $(echo "$miss_rate < ${best_miss_rates[$app]}" | bc) -eq 1 ]; then
            best_miss_rates[$app]=$miss_rate
            best_configs[$app]=$config
        fi
    done
done

# Output the best configuration and its miss rate for each app
for app in "${apps[@]}"; do
    echo "$app --dc=${best_configs[$app]} ${best_miss_rates[$app]}%"
done
