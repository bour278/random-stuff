// Function to calculate volume per minute and return results table
calcVolume:{[df;stats_df;first_start_time;first_end_time;last_start_time;last_end_time;tenor]
    // Filter for tenor
    tenor_df:select from df where Curvekey=tenor;
    
    // Calculate volume per minute
    tenor_df:update volume_per_minute:100*deltas CumulativeVolume from tenor_df;
    
    // Filter for time intervals
    first_df:select from tenor_df where NycTime within (first_start_time;first_end_time);
    last_df:select from tenor_df where NycTime within (last_start_time;last_end_time);
    all_df:select from tenor_df where NycTime within (first_start_time;last_end_time);
    
    // Calculate volume percentages
    first_volume_pct:sum first_df`volume_per_minute;
    last_volume_pct:sum last_df`volume_per_minute;
    
    // Get ADV from stats_df where Curvekey matches tenor
    tenor_stats:select from stats_df where Curvekey=tenor;
    adv:first tenor_stats[`adv];
    
    // Create results table
    ([]
        header:(
            "Estimated ADV Notional";
            "First Interval";
            "First Interval Volume percent";
            "First Interval Notional";
            "Second Interval";
            "Second Interval Volume percent";
            "Second Interval Notional"
        );
        value:(
            string[round[;0.01] 1000000*adv];
            string[first_start_time],"-",string[first_end_time];
            string[round[;0.01] first_volume_pct],"%";
            string[round[;0.01] 1000000*adv*first_volume_pct%100];
            string[last_start_time],"-",string[last_end_time];
            string[round[;0.01] last_volume_pct],"%";
            string[round[;0.01] 1000000*adv*last_volume_pct%100]
        )
    )
    };

// Example usage:
// calcVolume[df;stats_df;18:00:00.000;18:15:00.000;18:15:00.000;18:30:00.000;`2_YEAR]
