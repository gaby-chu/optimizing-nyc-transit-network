# Optimal Multimodal Flow in NYC: How Far Is Actual Travel From the Best Use of the Network?

Sep 28, 2026 · @gaby

## Summary

Hybrid work changed when and where New Yorkers travel, and many trips now combine the subway with a taxi, ride-hail, or bike. This project asks what the optimal flow of NYC's multimodal travel demand would be, how far actual travel is from it, and which network changes would close the gap.

Building on the multilayer network framework reviewed by Natera Orozco et al. (2021), the project builds a multilayer supply network (walk, bike, street, subway, and bus layers) from OpenStreetMap and GTFS schedules. It combines observed subway, Citi Bike, and Uber/Lyft/taxi trips into one mode-blind OD graph and routes that demand over the network in the way that minimizes total generalized cost (travel time, waiting, transfers, and fares), first without capacity limits and then with subway crowding. Comparing the optimal flow with what people actually do separates areas where the network works, where travelers choose costlier options, and where even the optimal flow is poor, which marks a true infrastructure gap. Network changes such as a new station or added frequency are tested by rerunning the optimal flow, and comparing weekdays, weekends, and years shows how the picture shifted with hybrid work.

## Motivation

**Travel changed shape, not just size.** In 2023, the MTA reported that commute ridership now peaks Tuesday through Thursday, and that weekend recovery (77% of 2019) outpaced weekday recovery (66%) ([MTA](https://www.mta.info/agency/new-york-city-transit/subway-bus-ridership-2023)). By mid-2026, one analysis of MTA data put weekend ridership near 90% of 2019 and weekdays near 75% ([Apollo](https://www.apollo.com/wealth/insights-news/insights/daily-spark/NYC-Subway-Ridership-Has-Recovered-on-Weekends-but-Not-on-Weekdays)). Discretionary trips now make up a larger share than commutes.

**The network was designed for the old pattern.** NYC's subway is largely radial, built to carry five-day commutes into Manhattan's core. If demand has shifted toward midweek peaks, weekends, and non-Manhattan trips, service allocated by the old pattern may be too much in some places and too little in others.

**A new shock arrived in 2025.** Congestion pricing began January 5, 2025. Subway ridership grew by almost 93 million trips that year, 7.7% over 2024, with the growth largely attributed to the toll ([PCAC](https://pcac.org/report/ridershipreturns/)). That tests whether the network can absorb demand pushed onto it.

**The gap.** Most reporting tracks systemwide ridership as a share of 2019. [PCAC](https://pcac.org/report/ridershipreturns/) mapped where subway ridership grew after congestion pricing. Few analyses combine subway, bike share, and ride-hail trips into one picture of demand, which is what shows where riders leave the subway to finish their trips another way.

## Baseline: multilayer transport networks

This project adopts the framework of [Natera Orozco, Alessandretti, Saberi, Szell & Battiston (2021)](https://arxiv.org/html/2111.02152v1), a review of multimodal urban mobility and multilayer transport networks. It treats each transport mode (walking, cycling, subway, bus, streets) as a layer of one network, with transfers between layers at shared locations. The review's opening example is a four-layer multiplex of Manhattan built from OpenStreetMap, so NYC is a natural test case.

**What the baseline provides.** Metrics for how well layers are integrated and how well the network can serve travel, most of which can be computed from public data:

| Metric | What it measures | Use in this project |
| --- | --- | --- |
| Overlap census | Share of nodes reachable by each combination of modes | Which neighborhoods are reachable by only one or two modes |
| Interdependence | Share of shortest paths that use two or more layers | How much trips depend on transfers, by origin |
| Spatial outreach | Average distance reachable within a travel-time budget | Accessibility by station and neighborhood |
| Betweenness centrality | Shortest paths through a node, assuming uniform demand | Compared against observed OD-weighted load |
| Synchronization inefficiency | Schedule-based travel time relative to the ideal minimum, minus one | Time lost to waits and transfers, by hour and day |
| Flow vs. network comparison (non-negative matrix factorization) | Whether transit serves commuting flows | The closest precedent for an adequacy test |

**Where this project extends the baseline.**

- **Real demand, not uniform demand.** The review notes that betweenness is a proxy for flow when mobility data are missing. NYC's origin-destination estimates let this project test that proxy directly and replace it with observed flows.
- **An adequacy test for a large city after hybrid work.** The review describes an earlier matrix-factorization comparison of commuting flows and transit networks in France, which found Paris's system met overall demand while smaller cities' systems did not. This project applies that idea to NYC with demand that changed after 2021.
- **Shared mobility.** The review names integrating bike share and other shared services into multimodal models as an open challenge. Citi Bike and Uber/Lyft trips are included here as layers.
- **Time variation.** The review notes that many studies rely on schedules and static networks. This project computes metrics by hour and day of week.
- **Equity.** The review frames sustainable mobility as social access to the city but does not measure who gets that access. This project maps the metrics against income, race, car ownership, and work-from-home rates.

**From measurement to optimal flow.** The review's metrics describe a network's structure. This project routes observed multimodal demand over that network optimally and compares the result with actual travel. The review covers the building blocks: route choice by travel-time minimization (Wardrop's principles), multimodal network design as a bilevel problem, and congestion models where faster layers draw trips to transfer hubs.

## Research questions

**Main question:** What is the optimal flow of NYC's multimodal travel demand, how far is actual travel from it, and which network changes close the gap?

### First stage: demand and the uncapacitated optimum

1. **Demand structure.** When subway, bike share, and ride-hail trips are combined into one mode-blind OD graph, which zones act as hubs, and which flows are hub-to-hub trunks vs. hub-to-satellite feeders?
2. **Optimal flow without crowding.** If every trip took its lowest-cost path on the multilayer network, which modes and routes would carry it?
3. **Actual vs. optimal.** Where does actual mode use match the optimum, and where do travelers take costlier options such as taxis when transit is nearly as good?

### Second stage: crowding, gaps, and fixes

4. **Optimal flow with crowding.** When subway travel time rises with load, how does the system-optimal flow redistribute trips across lines and modes?
5. **True gaps.** Which zone pairs are poorly served even under the optimal flow?
6. **Interventions.** How much does a new station or added frequency at the top gaps reduce total cost and bring the network closer to serving demand?
7. **Change over time.** How do the optimal flow and the gaps differ between weekdays and weekends, and between earlier years and 2026?
8. **Equity.** Are the gaps, and the gains from fixing them, concentrated in lower-income and low-car neighborhoods?

## Data sources and verification

Every core dataset is public and free; the subway origin-destination estimates are what make a network analysis of demand possible. Coverage was checked on the publisher's catalog page unless marked "to confirm."

### Mobility (demand)

| Dataset | Coverage | Use | Caveats |
| --- | --- | --- | --- |
| [MTA Subway Origin-Destination Ridership Estimate](https://catalog.data.gov/dataset/mta-subway-origin-destination-ridership-estimate-beginning-2025) | Yearly files for [2021](https://data.ny.gov/en/Transportation/MTA-Subway-Origin-Destination-Ridership-Estimate-2/rapa-97zv), [2022](https://data.ny.gov/en/Transportation/MTA-Subway-Origin-Destination-Ridership-Estimate-2/nqnz-e9z9), [2023](https://data.ny.gov/en/Transportation/MTA-Subway-Origin-Destination-Ridership-Estimate-2/uhf3-t34z), [2024](https://data.ny.gov/Transportation/MTA-Subway-Origin-Destination-Ridership-Estimate-2/jsu2-fbtj), [2025](https://data.ny.gov/en/Transportation/MTA-Subway-Origin-Destination-Ridership-Estimate-2/y2qv-fytt), and [2026 onward](https://catalog.data.gov/dataset/mta-subway-origin-destination-ridership-estimate-beginning-2026) | Demand network: flows between station complexes by month, day of week, and hour | Estimated by scaling up OMNY and MetroCard return-swipe data, not observed trips; no route or transfer information |
| [MTA Subway Hourly Ridership](https://data.ny.gov/Transportation/MTA-Subway-Hourly-Ridership-Beginning-February-202/wujg-7c2s) | Feb 2022 onward | Optional: flag unusual dates (holidays, outages) and cross-check OD totals; fare-payment class for the income extension | Entries only; not needed for the core model |
| [MTA Bus Hourly Ridership](https://data.ny.gov/Transportation/MTA-Bus-Hourly-Ridership-Beginning-February-2022/kv7t-n8in) | Feb 2022 onward | Bus demand by route and hour | Boardings, not origin-destination |
| [TLC trip records: High Volume FHV (Uber/Lyft), yellow taxi, green taxi](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) | 2019 onward | For-hire trips between taxi zones (observed OD layer); trip durations give car travel times that include real traffic | Zone level only; published with about a two-month delay; congestion fee column from 2025; the traditional FHV file is skipped because drop-off zones are often missing |
| [Citi Bike trip data](https://citibikenyc.com/system-data) | 2013 onward | Bike trips between stations | Service area excludes much of the outer boroughs |

### Commute timing (optional extension)

| Dataset | Coverage | Use | Caveats |
| --- | --- | --- | --- |
| [NYC DOT Citywide Mobility Survey](https://www.nyc.gov/html/dot/downloads/pdf/2024-cms-user-guide.pdf): [Person](https://data.cityofnewyork.us/Transportation/Citywide-Mobility-Survey-Person-2022/7qdz-u9hr) and [Day](https://catalog.data.gov/dataset/citywide-mobility-survey-day-2022) tables | Annual household travel survey; 2022 files confirmed, later years to check | Telework frequency, remote-work duration by day, commute mode, demographics; trains the person-level attendance model | Survey sample of a few thousand people a year; use provided weights |
| [ACS table B08302](https://api.census.gov/data/2019/acs/acs5/groups/B08302.html), time leaving home to go to work | Tract level, 5-year estimates | Departure-time distribution by home tract | Self-reported, typical day, no day-of-week detail |
| ACS worked-from-home share and industry by tract | Tract level | Covariates for how likely each area's workers are to telework | 5-year averages smooth recent change |
| [LODES](https://lehd.ces.census.gov/announcements.html) home-to-work flows | 2002–2023, block pairs, by industry and earnings | The home-to-work matrix: who could commute where | Shows jobs, not daily trips |
| [Kastle Back to Work Barometer](https://www.kastle.com/safety-wellness/getting-america-back-to-work/) | Weekly published figures, NYC metro | External check on office attendance by day of week | Proprietary badge data from participating office buildings; only published summaries are available |

These sources agree on the midweek office peak that a commute model would need to reproduce. In the week of Dec 8, 2025, Kastle reported a 66% Tuesday peak across its 10-city barometer, and NYC weekly occupancy reached 59.5% of the pre-pandemic baseline ([Kastle](https://www.kastle.com/resource/kastle-back-to-work-barometer-hits-all-time-post-pandemic-highs/)).

### Transport supply

| Dataset | Coverage | Use | Caveats |
| --- | --- | --- | --- |
| MTA GTFS static schedules (subway and bus) | Current feed on data.ny.gov ([MTA open data list](https://www.mta.info/document/152191)) | Supply network: routes, stops, frequency by hour and day | Past feeds for 2021–2024 must come from an archive (to confirm source) |
| MTA bus route shapes and stops | On data.ny.gov (to confirm exact dataset) | Bus layer geometry | — |
| [NYC bike lane network](https://data.cityofnewyork.us/dataset/New-York-City-Bike-Routes-Map-/9e2b-mctv) | Current network with install dates | Bike layer | — |
| NYC taxi zones | TLC shapefile ([TLC](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)) | Common zones to join FHV, subway, and census data | Zones are much larger than station catchments |

OpenStreetMap (via `OSMnx` or `pyrosm`) supplies the pedestrian, bicycle, and street layers, as in the baseline's Manhattan multiplex ([Natera Orozco et al.](https://arxiv.org/html/2111.02152v1)).

### Equity

| Dataset | Use |
| --- | --- |
| ACS 5-year estimates by tract (income, race and ethnicity, vehicles available, worked from home, occupation, commute time) | Neighborhood equity variables; share who can work from home |
| [LODES workplace and residence files](https://lehd.ces.census.gov/announcements.html) | Low-wage jobs by location, as a check on the income tiers |
| [Subway Hourly Ridership](https://data.ny.gov/Transportation/MTA-Subway-Hourly-Ridership-Beginning-February-202/wujg-7c2s) fare-payment class | Reduced-fare and low-income fare use by station. Fair Fares OMNY cards began in February 2025 ([OMNY](https://en.wikipedia.org/wiki/OMNY)); exact fare classes in the dataset to confirm |

### Natural experiment

| Dataset | Coverage | Use |
| --- | --- | --- |
| [MTA Congestion Relief Zone Vehicle Entries](https://catalog.data.gov/dataset/mta-congestion-relief-zone-vehicle-entries-beginning-2025) | Jan 5, 2025 onward, 10-minute intervals | Vehicle entries by crossing point and vehicle class |
| [MTA CBD taxi zones](https://catalog.data.gov/dataset/mta-central-business-district-taxi-zones) | Current | Flags which TLC zones are inside the toll zone |

### Still to confirm

- Source for historical GTFS feeds (2021–2024).
- Fare-payment classes in the hourly ridership file.
- Whether Columbia provides access to commercial phone-based mobility data, in case the course expects GPS-style data.

## Methods

The first stage builds the multilayer network and a mode-blind OD graph, computes the optimal flow without capacity limits, and compares it with actual travel. The second stage adds subway crowding, identifies true gaps, and tests network changes by rerunning the optimal flow. All work is in Python (OSMnx or pyrosm for OpenStreetMap layers, peartree for GTFS-to-graph, pymnet for multilayer metrics, `networkx` or `igraph`, `gtfs-kit`, `r5py`, `geopandas`, `statsmodels`).

### First stage: demand and the uncapacitated optimum

**Zones, not stations.** Each mode uses different locations (subway stations, bus stops, Citi Bike docks, taxi zones), so demand is built on one common set of zones. TLC taxi zones are the simplest choice because the for-hire trip data already uses them; census tracts are a finer alternative. Each zone connects to the network through walking links to nearby stations, stops, and docks.

**What "optimal" means.** Every path is scored by generalized cost, so that time and money are compared fairly:

```latex
c_{p} = t^{\mathrm{walk}}_{p} + t^{\mathrm{ride}}_{p} + \alpha\, t^{\mathrm{wait}}_{p} + \beta\, n^{\mathrm{xfer}}_{p} + \frac{\text{fare}_{p}}{\text{VOT}}
```

Waiting is weighted more than riding (α about 2), each transfer adds a penalty (β of a few minutes), and fares are converted to minutes with a value of time (VOT). Without the fare term, the optimum would put nearly everyone on transit and every taxi trip would look wrong. The weights come from standard values in the transport literature and are tested in a sensitivity check.

#### Steps

1. **Multilayer supply network.** Walk, bike, and street layers from OpenStreetMap; subway and bus layers from GTFS (ride edges with scheduled run time, boarding edges with a wait of half the headway, transfer edges with walking time plus a penalty); car travel times from TLC trip durations; zone connectors.
2. **Observed OD graphs by mode.** Map subway stations and Citi Bike docks to zones, convert every mode to the same units (average trips per weekday hour), and keep day of week and hour. A first version for January 2026 (subway, Citi Bike, and Uber/Lyft/taxi) is already built; add a warmer month and the same month from an earlier year for comparison.
3. **Mode-blind OD graph.** Sum the modes for each zone pair and time slice, and keep the actual mode mix as an edge attribute.
4. **Demand structure.** Rank zones by total trips; use Leiden community detection and a core–periphery split to separate hubs from satellites; label flows hub–hub, hub–satellite, or satellite–satellite.
5. **Uncapacitated optimal flow.** With no crowding, the optimal flow sends each zone pair's trips along its lowest-cost path. Run **Dijkstra** on the multilayer network for every origin to get the optimal mode, route, and cost for each zone pair, and the resulting load on every segment.
6. **Actual vs. optimal.** For each zone pair, compare the actual mode mix with the optimal mode and the cost gap between them. Summarize by flow type: hub–hub pairs where actual matches optimal mean the network works; pairs where people use taxis though transit costs only slightly more point to preference, reliability, or information; pairs where the optimal path itself is slow point to a network gap.
7. **Last-mile signature.** At top hubs, compare the hourly pattern of subway arrivals with taxi, ride-hail, and Citi Bike departures to nearby zones. Trips can't be linked across modes, so this is an aggregate signal that supports the actual-vs-optimal comparison.

### Second stage: crowding, gaps, and fixes

1. **Optimal flow with crowding.** Make each subway segment's travel time rise as its load approaches capacity (a standard volume-delay function), and solve for the system optimum, the flow that minimizes total cost for everyone, with the **Frank–Wolfe** algorithm. Each iteration runs the same Dijkstra assignment, so it builds directly on the first stage. Keep crowding to the subway and to the weekday morning peak.

   ```latex
   \min_{x} \; \sum_{e} x_e \, c_e(x_e) \quad \text{s.t. flows on paths sum to demand } q_{od} \text{ for every zone pair}
   ```

2. **Price of crowding.** Compare total cost and segment loads with and without capacity limits to find where crowding forces trips onto worse paths.
3. **True gaps.** Zone pairs whose optimal cost stays high relative to straight-line distance, or that rely on taxi even in the optimum, are network gaps. Map them.
4. **Interventions.** At the top gaps, test (a) a new subway station inserted on the nearest line, with an extra stop time for trains passing through, and (b) added frequency on a crowded line, holding total train-hours fixed. Rerun the optimal flow and report the reduction in total cost and in the actual-vs-optimal gap.
5. **Change over time.** Repeat the optimal flow and gap analysis for weekday vs. weekend demand and earlier years vs. 2026.

**Extensions if time allows:** a bike-lane or bus-route intervention; a user-equilibrium flow (each traveler minimizing their own cost) to compare with the system optimum; the commute model to test work-from-home scenarios.

## Equity analysis

The equity question is whether the gaps between actual and optimal travel, and the gains from fixing them, fall on lower-income and low-car neighborhoods, or mostly on areas where people can already afford alternatives.

**Why neighborhoods, not individual riders.** The trip data records where trips start and end, not who takes them or why. So equity is measured by tagging each zone with the income of its neighborhood, which is observable and defensible, rather than guessing at who individual riders are.

### How zones are tagged

1. Give each zone the population-weighted median household income of its census tracts (ACS table B19013).
2. Group zones into income tiers (lowest, middle, and highest third).
3. Add the share of households with no car (ACS table B08201) as a second tag. Low-income, low-car areas have the fewest alternatives when the network falls short.
4. Each trip takes the tier of its origin zone, since that is where riders live for morning commutes.

### What is measured, by income tier

| Measure | What it shows |
| --- | --- |
| Optimal cost per trip | How well the network can serve each tier at best |
| Actual-vs-optimal cost gap | How far actual travel is from the best available option |
| Share of trips in true-gap zone pairs | Who the network fails |
| Cost reduction from each intervention | Who benefits from each fix |

**The key test.** Rank interventions by total cost reduction, then by cost reduction for the lowest-income tier. If the top picks differ, report both and the trade-off between them.

**A caution on taxis.** Taxi and ride-hail use reflects income as well as need, so a high taxi share in a wealthy zone is not the same as a network gap. The fare term in the generalized cost and the income tags keep these apart.

## Timeline, deliverables, and risks

The midterm is Oct 26, 2026 and the final is Dec 14, 2026. The midterm presents the mode-blind demand graph, the uncapacitated optimal flow, and the actual-vs-optimal comparison; the final adds subway crowding, true gaps, interventions, change over time, and equity.

### Weekly plan

| Week | Focus | Deliverable |
| --- | --- | --- |
| Oct 5–11 | Observed demand | OD graph for January 2026 (subway, Citi Bike, Uber/Lyft/taxi) — done |
| Oct 12–18 | Demand and supply | Units and zones harmonized; mode-blind OD graph; hubs and communities; all supply layers built (walk, bike, street, subway, bus, car times, zone connectors) |
| Oct 19–25 | Uncapacitated optimum | Dijkstra optimal flow with generalized cost; segment loads; actual vs. optimal by flow type; last-mile signature; midterm slides by Oct 24 |
| Oct 26 | **Midterm** | Presentation |
| Oct 26–Nov 1 | More demand | Warmer month and earlier-year OD graphs; fixes from midterm feedback |
| Nov 2–8 | Crowding | Frank–Wolfe system optimum on the subway, weekday AM; checked on a small test network |
| Nov 9–15 | Gaps | Price of crowding; map of true gaps |
| Nov 16–22 | Interventions | New-station and added-frequency tests at the top gaps |
| Nov 23–29 | Time and sensitivity (light week) | Weekday vs. weekend and earlier year vs. 2026; sensitivity to cost weights |
| Nov 30–Dec 6 | Equity | Results by income tier; final figures |
| Dec 7–13 | Writing | Report, slides, and cleaned code |
| Dec 14 | **Final** | Submission and presentation |

### Midterm deliverables

- [ ] Mode-blind OD graph for January 2026 in common units
- [ ] Multilayer supply network with all layers
- [ ] Map of hubs, communities, and flow types
- [ ] Uncapacitated optimal flow and segment loads
- [ ] Actual vs. optimal comparison by flow type
- [ ] Last-mile signature at top hubs

### Final deliverables

- [ ] Optimal flow with subway crowding and the price of crowding
- [ ] Map of true gaps
- [ ] Intervention results (new station, added frequency)
- [ ] Change over time (weekday vs. weekend, earlier year vs. 2026)
- [ ] Equity results by income tier, report, and code

**If behind schedule, cut in this order:** commute-model extension, user-equilibrium comparison, earlier-year comparison, then the crowded optimum (keep the uncapacitated optimum and report segment loads against capacity instead).

### Risks and fallbacks

| Risk | Fallback |
| --- | --- |
| Trips can't be linked across modes, so last-mile trips are inferred | State it as a limitation; rely on timing and distance patterns, and check against known transfer hubs |
| Modes come in different units (subway averages vs. raw trip counts) | Convert everything to average trips per weekday hour before combining |
| January has low biking and holidays | Add a warmer month and drop holiday weeks |
| Generalized-cost weights (wait, transfer, value of time) are assumptions | Use standard literature values and report sensitivity |
| Taxi use reflects income, not just need | Keep the fare term in the cost and report results by income tier |
| Frank–Wolfe is slow or converges poorly | Limit crowding to the subway and the weekday AM peak, cap iterations, and report the convergence gap; fall back to the uncapacitated optimum |
| Bus has no public OD data | Include bus in the supply network for travel times; note bus riders are missing from the demand graph |
| Zones are coarse for placing a new station | Use census tracts in the busiest areas or test sensitivity to zone size |
| Each intervention means rerunning the optimal flow | Test only the top-ranked gaps and reuse shortest-path trees where nothing changed |
| Scope too large for Dec 14 | Follow the cut order above |

## References

### Baseline paper

- Natera Orozco, L. G., Alessandretti, L., Saberi, M., Szell, M. & Battiston, F. (2021). [Multimodal urban mobility and multilayer transport networks](https://arxiv.org/html/2111.02152v1). arXiv 2111.02152. Works it reviews that this project draws on (see its reference list): Aleta et al. (2017) on superlayers; Strano et al. (2015) on spatial outreach and NYC betweenness; Gallotti & Barthelemy (2014) on synchronization inefficiency; Alessandretti et al. (2016) on comparing commuting flows with transit networks; Natera Orozco et al. (2020) on the overlap census; Zheng et al. (2018) on behavioral layer coupling.

### Reports and articles

- MTA. [Subway and bus ridership for 2023](https://www.mta.info/agency/new-york-city-transit/subway-bus-ridership-2023).
- Apollo. [NYC subway ridership has recovered on weekends but not on weekdays](https://www.apollo.com/wealth/insights-news/insights/daily-spark/NYC-Subway-Ridership-Has-Recovered-on-Weekends-but-Not-on-Weekdays) (July 2026).
- PCAC. [Ridership Returns: Mapping post-congestion pricing ridership trends](https://pcac.org/report/ridershipreturns/) (March 2026).
- MTA. [New Congestion Relief Zone data captures faster commutes and surging express bus ridership](https://www.mta.info/press-release/new-congestion-relief-zone-data-captures-magnitude-of-faster-commutes-drivers-and-bus).
- MTA. [The most detailed view of NYC traffic (so far)](https://www.mta.info/article/most-detailed-view-of-nyc-traffic-so-far) (CRZ data explainer).
- Kastle Systems. [Back to Work Barometer](https://www.kastle.com/safety-wellness/getting-america-back-to-work/) and [post-pandemic high, Dec 2025](https://www.kastle.com/resource/kastle-back-to-work-barometer-hits-all-time-post-pandemic-highs/).

### Datasets

- MTA Subway Origin-Destination Ridership Estimate: [2021](https://data.ny.gov/en/Transportation/MTA-Subway-Origin-Destination-Ridership-Estimate-2/rapa-97zv), [2022](https://data.ny.gov/en/Transportation/MTA-Subway-Origin-Destination-Ridership-Estimate-2/nqnz-e9z9), [2023](https://data.ny.gov/en/Transportation/MTA-Subway-Origin-Destination-Ridership-Estimate-2/uhf3-t34z), [2024](https://data.ny.gov/Transportation/MTA-Subway-Origin-Destination-Ridership-Estimate-2/jsu2-fbtj), [2025](https://catalog.data.gov/dataset/mta-subway-origin-destination-ridership-estimate-beginning-2025), [2026 onward](https://catalog.data.gov/dataset/mta-subway-origin-destination-ridership-estimate-beginning-2026)
- [MTA Subway Hourly Ridership](https://data.ny.gov/Transportation/MTA-Subway-Hourly-Ridership-Beginning-February-202/wujg-7c2s)
- [MTA Bus Hourly Ridership](https://data.ny.gov/Transportation/MTA-Bus-Hourly-Ridership-Beginning-February-2022/kv7t-n8in)
- [MTA Open Data update to the Board, Sept 2024](https://www.mta.info/document/152191) (includes GTFS static data)
- [MTA Congestion Relief Zone Vehicle Entries](https://catalog.data.gov/dataset/mta-congestion-relief-zone-vehicle-entries-beginning-2025)
- [MTA CBD taxi zones](https://catalog.data.gov/dataset/mta-central-business-district-taxi-zones)
- [TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [Citi Bike system data](https://citibikenyc.com/system-data)
- [NYC bike routes](https://data.cityofnewyork.us/dataset/New-York-City-Bike-Routes-Map-/9e2b-mctv)
- [LEHD LODES (2002–2023)](https://lehd.ces.census.gov/announcements.html)
- [OMNY fare programs](https://en.wikipedia.org/wiki/OMNY)
- NYC DOT [Citywide Mobility Survey user guide](https://www.nyc.gov/html/dot/downloads/pdf/2024-cms-user-guide.pdf); [Person 2022](https://data.cityofnewyork.us/Transportation/Citywide-Mobility-Survey-Person-2022/7qdz-u9hr) and [Day 2022](https://catalog.data.gov/dataset/citywide-mobility-survey-day-2022) tables
- [ACS B08302, time leaving home to go to work](https://api.census.gov/data/2019/acs/acs5/groups/B08302.html)
