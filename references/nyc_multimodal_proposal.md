# How Does NYC's Optimal Multimodal Network Change When Mobility Patterns Change?

Sep 28, 2026 · Gaby

## Summary

Hybrid work made commuting a variable: how many days people go to the office, when they leave home, and who works remotely all shift over time and differ across the city. This project asks how the optimal multimodal transit network changes as those mobility patterns change, and which parts of the network are robust to them.

Building on the multilayer network framework reviewed by Natera Orozco et al. (2021), the first stage builds one commute model that turns where people live and work (LODES), how often they go in, and when they leave into total trips between zones, then splits them across subway, bus, Citi Bike, and Uber/Lyft/taxi with a mode choice model. At today's settings it should reproduce observed subway, Citi Bike, and for-hire trips. It also builds a multilayer supply network (walk, bike, street, subway, and bus layers) from OpenStreetMap and GTFS schedules. The second stage varies the model's parameters (office days per week, which days, and departure-time spread), producing a new OD graph for each scenario, lets riders switch modes, routes each scenario's demand with shortest paths on the multilayer network, optimizes subway and bus service within today's vehicle-hour budget, and measures how the optimal network shifts. It also reports which neighborhoods gain or lose service in each scenario, with attention to lower-income and low-car neighborhoods.

## Motivation

**Travel changed shape, not just size.** In 2023, the MTA reported that commute ridership now peaks Tuesday through Thursday, and that weekend recovery (77% of 2019) outpaced weekday recovery (66%) ([MTA](https://www.mta.info/agency/new-york-city-transit/subway-bus-ridership-2023)). By mid-2026, one analysis of MTA data put weekend ridership near 90% of 2019 and weekdays near 75% ([Apollo](https://www.apollo.com/wealth/insights-news/insights/daily-spark/NYC-Subway-Ridership-Has-Recovered-on-Weekends-but-Not-on-Weekdays)). Discretionary trips now make up a larger share than commutes.

**The network was designed for the old pattern.** NYC's subway is largely radial, built to carry five-day commutes into Manhattan's core. If demand has shifted toward midweek peaks, weekends, and non-Manhattan trips, service allocated by the old pattern may be too much in some places and too little in others.

**A new shock arrived in 2025.** Congestion pricing began January 5, 2025. Subway ridership grew by almost 93 million trips that year, 7.7% over 2024, with the growth largely attributed to the toll ([PCAC](https://pcac.org/report/ridershipreturns/)). That tests whether the network can absorb demand pushed onto it.

**The gap.** Most reporting tracks systemwide ridership as a share of 2019. [PCAC](https://pcac.org/report/ridershipreturns/) mapped where ridership grew after congestion pricing. This project goes further by comparing station-to-station demand with scheduled supply as networks, by hour and day of week, asking who the mismatch affects, and testing how the best service plan would change if commuting patterns shift again.

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

**From measurement to scenarios.** The review's metrics describe a network under one demand pattern. This project treats demand as a set of parameters and asks how the metrics and the optimal network respond when those parameters change. The review covers the building blocks: multimodal network design as a bilevel problem (planners set service, travelers respond by shortest or cheapest paths), frequency design under user equilibrium, and congestion models where changes in one layer's speed or demand shift trips to transfer hubs. None of the reviewed work varies commuting frequency or timing to see how the optimal network moves.

## Research questions

**Main question:** How does the optimal multimodal network change when mobility patterns change?

**First stage: model mobility and the network**

1. **Commute model.** Can a model built from where people live and work, how often they go in, and when they leave reproduce today's observed trips on the subway, Citi Bike, and Uber/Lyft/taxi?
2. **Mode choice.** How well do travel times and transfers on each layer of the network explain which mode people take between two zones?
3. **Baseline network.** With today's demand, where are the multilayer network's bottlenecks and gaps, measured by shortest-path load and the baseline multilayer metrics?

**Second stage: change the patterns, re-optimize**

4. **Sensitivity.** When office days per week, departure-time spread, or peak timing change, how do loads, mode shares, and the optimal multimodal service plan change?
5. **What moves and what stays.** Which routes, segments, and transfer points are needed in every scenario, and which matter only under certain patterns?
6. **Tipping points.** Are there parameter values where the optimal network changes sharply (e.g., a line that should gain or lose peak frequency)?
7. **Robust plan.** Which single service plan performs acceptably across all plausible scenarios?
8. **Equity.** Does each scenario's optimal plan help or hurt lower-income neighborhoods, especially when remote work is concentrated among higher-income workers?

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
| [LODES home-to-work flows](https://lehd.ces.census.gov/announcements.html) | 2002–2023 | Expected commutes by census block pair, industry, and earnings | Shows where people work, not whether they commute that day |

### Commute timing and frequency (for the commute model)

| Dataset | Coverage | Use | Caveats |
| --- | --- | --- | --- |
| [NYC DOT Citywide Mobility Survey](https://www.nyc.gov/html/dot/downloads/pdf/2024-cms-user-guide.pdf): [Person](https://data.cityofnewyork.us/Transportation/Citywide-Mobility-Survey-Person-2022/7qdz-u9hr) and [Day](https://catalog.data.gov/dataset/citywide-mobility-survey-day-2022) tables | Annual household travel survey; 2022 files confirmed, later years to check | Telework frequency, remote-work duration by day, commute mode, demographics; trains the person-level attendance model | Survey sample of a few thousand people a year; use provided weights |
| [ACS table B08302](https://api.census.gov/data/2019/acs/acs5/groups/B08302.html), time leaving home to go to work | Tract level, 5-year estimates | Departure-time distribution by home tract | Self-reported, typical day, no day-of-week detail |
| ACS worked-from-home share and industry by tract | Tract level | Covariates for how likely each area's workers are to telework | 5-year averages smooth recent change |
| [LODES](https://lehd.ces.census.gov/announcements.html) home-to-work flows | 2002–2023, block pairs, by industry and earnings | The home-to-work matrix: who could commute where | Shows jobs, not daily trips |
| [Kastle Back to Work Barometer](https://www.kastle.com/safety-wellness/getting-america-back-to-work/) | Weekly published figures, NYC metro | External check on office attendance by day of week | Proprietary badge data from participating office buildings; only published summaries are available |

These sources agree on the pattern the model must reproduce. In the week of Dec 8, 2025, Kastle reported a 66% Tuesday peak across its 10-city barometer, and NYC weekly occupancy reached 59.5% of the pre-pandemic baseline ([Kastle](https://www.kastle.com/resource/kastle-back-to-work-barometer-hits-all-time-post-pandemic-highs/)).

### Transport supply

| Dataset | Coverage | Use | Caveats |
| --- | --- | --- | --- |
| MTA GTFS static schedules (subway and bus) | Current feed on data.ny.gov ([MTA open data list](https://www.mta.info/document/152191)) | Supply network: routes, stops, frequency by hour and day | Past feeds for 2021–2024 must come from an archive (to confirm source) |
| MTA bus route shapes and stops | On data.ny.gov (to confirm exact dataset) | Bus layer geometry |  |
| [NYC bike lane network](https://data.cityofnewyork.us/dataset/New-York-City-Bike-Routes-Map-/9e2b-mctv) | Current network with install dates | Bike layer |  |
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

The first stage builds two models, one of commute demand and one of the multilayer network, and checks both against observed ridership. The second stage perturbs the demand model's parameters, re-optimizes the network for each scenario, and measures what changes. All work is in Python (OSMnx or pyrosm for OpenStreetMap layers, peartree for GTFS-to-graph, pymnet for multilayer metrics, `networkx` or `igraph`, `gtfs-kit`, `r5py`, `geopandas`, `statsmodels`).

### First stage: build the multimodal demand model and the baseline

**Zones, not stations.** Each mode uses different locations (subway stations, bus stops, Citi Bike docks, taxi zones), so demand is built on one common set of zones. TLC taxi zones are the simplest choice because the for-hire trip data already uses them; census tracts are a finer alternative. Each zone connects to the network through walking links to nearby stations, stops, and docks.

**One model, observed and modeled OD graphs.** OD graphs have zones as nodes and trips between them as edge weights.

|  | Observed OD graphs | Modeled OD graph |
| --- | --- | --- |
| Source | [MTA subway OD estimates](https://catalog.data.gov/dataset/mta-subway-origin-destination-ridership-estimate-beginning-2025), [Citi Bike trips](https://citibikenyc.com/system-data), and [TLC trip records](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page), each aggregated to zones | The commute model with mode choice |
| What it shows | Today's trips on each mode that has OD data | Total trips between zones, split by mode |
| Role | Baseline and calibration target | Regenerated with different settings to create scenarios |
| Can it change? | No, it records the past | Yes: change a setting, get a new OD graph |

At today's settings, the modeled subway, Citi Bike, and for-hire trips should closely match the observed ones. Bus has no public OD data, so modeled bus trips are checked against route boardings instead.

**Why a model is needed.** Scaling the observed graphs would shrink every zone pair by the same percentage, and would keep every rider on the mode they use today. The model knows from LODES which pairs are commute-heavy, so a change in office attendance hits those pairs harder. Its mode choice step lets riders switch modes when travel times change, which is what makes the optimal network multimodal.

**The model** has two parts.

1. **Total trips between zones** (trip distribution, the first steps of the standard four-step travel demand model), for origin zone o, destination d, day of week w, and hour h:

```latex
T_{od,w,h} = W_{od} \cdot a_w \cdot s_h + N_{od,w,h}
```

2. **Mode choice** (multinomial logit), splitting those trips across modes k:

```latex
T^{k}_{od,w,h} = T_{od,w,h} \cdot \frac{\exp(V^{k}_{od})}{\sum_{j} \exp(V^{j}_{od})}, \qquad V^{k}_{od} = \beta^{k}_{0} + \beta_{t}\, t^{k}_{od} + \beta_{x}\, x^{k}_{od} + \beta_{c}\, c^{k}_{od}
```

- W: workers who live in zone o and work in zone d ([LODES](https://lehd.ces.census.gov/announcements.html))
- a: share of workers who go in on day w
- s: share of commuters leaving home in hour h
- N: non-commute trips (fitted)
- k: subway, bus, Citi Bike, for-hire (Uber/Lyft/taxi), and other (car, walking) as one remaining group
- t, x, c: travel time, transfers, and cost on mode k between the two zones, from shortest paths on the multilayer network and published fares
- the β values are fitted

**Steps**

1. **Multilayer supply network.** Walk, bike, and street layers from OpenStreetMap; subway and bus layers from GTFS (ride edges with scheduled run time, boarding edges with a wait of half the headway, transfer edges with walking time plus a penalty); and zone connectors.
2. **Zones and W.** Assign LODES census blocks to zones and sum workers by zone pair.
3. **Observed OD graphs by mode.** Aggregate subway OD (station to its zone), Citi Bike trips (dock to its zone), and TLC trips (already by zone) to the same zones and time slices.
4. **Today's settings, measured from data.** Take a (share going in by day) and s (departure timing) from the day-of-week and hourly patterns in the observed data or the [Citywide Mobility Survey](https://www.nyc.gov/html/dot/downloads/pdf/2024-cms-user-guide.pdf). Fit s as a curve with a center and a spread so scenarios can change either one.
5. **Travel times by mode.** Run **Dijkstra** shortest paths on each mode's layers to get travel time and transfers for every zone pair. For car and for-hire travel, use median trip durations from the TLC taxi and Uber/Lyft records by zone pair and hour, which include real traffic, instead of OpenStreetMap speed limits; use the OpenStreetMap street network only for zone pairs with too few trips.
6. **Calibrate.** Fit the mode choice parameters and the non-commute term so that modeled trips match the observed subway, Citi Bike, and for-hire OD graphs, and modeled mode shares by home zone match ACS commute mode shares (table B08301, which also covers bus, car, and walking). Use maximum likelihood with a count model (Poisson or negative binomial) on the observed modes, in `statsmodels`, `scipy.optimize`, or a discrete-choice package such as Biogeme.
7. **Validate.** For each mode, plot predicted vs. observed trips by zone pair on log-log axes and report R². Check modeled bus trips against route boardings, mode shares against ACS, and the day-of-week and hourly shapes. Predict a held-out month or year, and compare a with [Kastle's](https://www.kastle.com/safety-wellness/getting-america-back-to-work/) published office attendance by day.
8. **Baseline assignment and metrics.** Route each mode's trips on the multilayer network with Dijkstra to get loads on every subway and bus segment, and compute the baseline multilayer metrics from [Natera Orozco et al. (2021)](https://arxiv.org/html/2111.02152v1).

**Later extension: income groups.** Split W into the three LODES earnings groups and give each group its own share going in by day, from the Citywide Mobility Survey. The formulas and calibration stay the same. This enables the remote-work and equity scenarios.

### Second stage: change the patterns, re-optimize

**Scenario parameters.** Each is a knob in the demand model:

| Parameter | What changes in the model | Range to test |
| --- | --- | --- |
| Office days per week | a scaled up or down | 2, 3, 4, 5 days |
| Which days | Pattern of a across the week | Concentrated Tuesday–Thursday vs. spread evenly |
| Departure-time spread | Width of s | Narrower (sharper peak) to wider (peak spreading) |
| Peak timing | Center of s | Earlier or later by up to an hour |
| Non-commute travel | N | Lower, current, higher |

Added with the income-group extension: who works remotely (concentrated among higher earners vs. spread evenly) and return-to-office mandates for selected groups.

Sample combinations with a Latin hypercube design (`scipy.stats.qmc`) so a manageable number of runs covers the space.

**For each scenario:**

1. Generate total trips between zones from the commute model and split them by mode with the fitted mode choice model.
2. Assign each mode's trips to the multilayer network with Dijkstra shortest paths (upgrading to frequency-based assignment with crowding if time allows).
3. Optimize service: reallocate subway and bus frequencies across routes and time slices within today's vehicle-hour budget, minimizing total generalized cost. After each change, rerun mode choice and assignment so riders can switch modes:

```latex
\min_{f} \; \sum_{od} w_{od} \, q_{od} \left( t^{\mathrm{ivt}}_{od} + \alpha \, t^{\mathrm{wait}}_{od}(f) + \beta \, n^{\mathrm{xfer}}_{od} + \gamma \, c_{od}(f) \right) \quad \text{s.t.} \; \sum_{r} h_r f_r \le H, \; f_r \ge f^{\min}_r
```

q is scenario demand for each zone pair and mode, the terms are in-vehicle time, wait (half the headway), transfers, and crowding, f is frequency on route r, and H is today's vehicle-hour budget. Solve with a greedy marginal-benefit heuristic: repeatedly move a vehicle-hour from the route and period where it saves the least to where it saves the most, re-running the shortest-path assignment after each move.

**Compare optimal networks across scenarios.**

- **How much the plan moves:** change in optimal frequency by route and period; distance between plans.
- **Which bottlenecks persist:** overlap (Jaccard) of the most crowded segments; rank correlation of segment loads.
- **Sensitivity:** fit a surrogate model (Gaussian process or regression) of optimal frequencies on the scenario parameters, and compute Sobol sensitivity indices (`SALib`) to rank which parameter matters most.
- **Tipping points:** parameter values where a route's optimal frequency jumps.
- **Cost of not adapting:** extra generalized cost of keeping today's schedule under each scenario.
- **Robust plan:** choose the plan with the smallest worst-case regret across scenarios (minimax regret), and report where it differs from today's service.

**Additional levers if time allows:** Citi Bike dock locations and protected bike links, and new feeder or crosstown bus routes. Also check the model against the January 2025 congestion-pricing shift.

## Equity analysis

This analysis is added with the income-group extension, once the core model works. The equity question is whether changes in commuting patterns, and the service plans that respond to them, help or hurt lower-income neighborhoods. Remote work is mostly available to higher earners, so when office days fall, demand drops more on routes from wealthier areas, and an optimizer will move service toward the demand that remains.

**Why neighborhoods, not individual riders.** The subway OD data records where trips start and end, not who takes them or why. So equity is measured by tagging each station with the income of the neighborhood around it, which is observable and defensible, rather than guessing at who individual riders are.

**How stations are tagged.**

1. Give each station the median household income of the census tracts within about half a mile, weighted by population (ACS table B19013).
2. Group stations into income tiers (lowest, middle, and highest third).
3. Add the share of households with no car (ACS table B08201) as a second tag. Low-income, low-car areas are the riders with the fewest alternatives when service changes.
4. Each trip takes the tier of its origin station, since that is where riders live for morning commutes.

**What is measured for each income tier, in each scenario, compared with today's service:**

| Measure | What it shows |
| --- | --- |
| Change in average generalized travel time (wait, ride, transfers) | Whether trips from the tier get faster or slower |
| Change in trains per hour at the tier's stations | Whether service is added or cut where they live |
| Change in crowding on segments the tier's riders use | Whether remaining trips get more or less crowded |
| Change in spatial outreach (how far riders can get in 45 minutes) | Access to jobs and services, from [Natera Orozco et al. (2021)](https://arxiv.org/html/2111.02152v1) |
| Overlap census by tier | Whether lower-income areas rely on fewer modes |

**The key test.** When remote work grows mainly among higher earners, does an efficiency-only optimizer help or hurt lower-income neighborhoods? Either result is informative:

- **Helps:** their riders keep traveling, so service follows them.
- **Hurts:** their trips are off-peak, outer-borough, or long, which a plan focused on total travel time may deprioritize.

**Equity version of the optimization.** Rerun each scenario with higher weights on trips from lower-income, low-car stations, and a floor so no income tier's spatial outreach falls below today's level. Report how much total travel time the equity version costs, and which routes and hours differ between the two plans.

## Timeline, deliverables, and risks

The final is due Dec 21, 2026. Midterm date: to confirm with the course schedule.

**Midterm deliverables**

- [ ] Multilayer supply network (walk, bike, street, subway, bus) from GTFS and OpenStreetMap, with zone connectors
- [ ] Observed zone-level OD graphs for subway, Citi Bike, and for-hire trips
- [ ] Home-to-work matrix from LODES by zone
- [ ] Fitted commute and mode choice model, with validation by mode
- [ ] Baseline shortest-path assignment, segment loads, and multilayer metrics

**Final deliverables**

- [ ] Scenario design and generated OD matrices
- [ ] Optimal frequency plan for each scenario
- [ ] Comparison of optimal plans: what moves, what persists, tipping points
- [ ] Sensitivity ranking of parameters (surrogate model and Sobol indices)
- [ ] Robust plan by minimax regret
- [ ] Equity comparison across scenarios

**Risks and fallbacks**

| Risk | Fallback |
| --- | --- |
| Bus has no public OD data | Infer bus trips from the mode choice model; check against route boardings and ACS bus commute shares; state as a limitation |
| Car and walking trips are not observed | Group them as "other" in mode choice and calibrate their share to ACS commute mode shares |
| Mode choice model is hard to calibrate with several data sources | Start with subway vs. for-hire vs. Citi Bike only, then add bus and "other" |
| Zones are coarse for short trips | Use census tracts in Manhattan or test sensitivity to zone size |
| Subway OD data has no trip purpose, so commute and non-commute trips are mixed | Use LODES as the commute prior and weekday-vs-weekend and hourly structure to separate them |
| Historical GTFS for 2021–2024 is hard to find | Use the current schedule as the supply network for all scenarios |
| OD files are large | Filter to representative weekdays and hours; use Parquet and DuckDB |
| Re-optimizing the whole network for every scenario is slow | Optimize a corridor or one borough; use fewer scenarios; reuse shortest-path trees between runs |
| Scope too large for Dec 21 | Keep the demand model with mode choice, three or four core scenarios, and the plan comparison; drop surrogate modeling and additional levers |

## References

**Baseline paper**

- Natera Orozco, L. G., Alessandretti, L., Saberi, M., Szell, M. & Battiston, F. (2021). [Multimodal urban mobility and multilayer transport networks](https://arxiv.org/html/2111.02152v1). arXiv 2111.02152. Works it reviews that this project draws on (see its reference list): Aleta et al. (2017) on superlayers; Strano et al. (2015) on spatial outreach and NYC betweenness; Gallotti & Barthelemy (2014) on synchronization inefficiency; Alessandretti et al. (2016) on comparing commuting flows with transit networks; Natera Orozco et al. (2020) on the overlap census; Zheng et al. (2018) on behavioral layer coupling.

**Reports and articles**

- MTA. [Subway and bus ridership for 2023](https://www.mta.info/agency/new-york-city-transit/subway-bus-ridership-2023).
- Apollo. [NYC subway ridership has recovered on weekends but not on weekdays](https://www.apollo.com/wealth/insights-news/insights/daily-spark/NYC-Subway-Ridership-Has-Recovered-on-Weekends-but-Not-on-Weekdays) (July 2026).
- PCAC. [Ridership Returns: Mapping post-congestion pricing ridership trends](https://pcac.org/report/ridershipreturns/) (March 2026).
- MTA. [New Congestion Relief Zone data captures faster commutes and surging express bus ridership](https://www.mta.info/press-release/new-congestion-relief-zone-data-captures-magnitude-of-faster-commutes-drivers-and-bus).
- MTA. [The most detailed view of NYC traffic (so far)](https://www.mta.info/article/most-detailed-view-of-nyc-traffic-so-far) (CRZ data explainer).
- Kastle Systems. [Back to Work Barometer](https://www.kastle.com/safety-wellness/getting-america-back-to-work/) and [post-pandemic high, Dec 2025](https://www.kastle.com/resource/kastle-back-to-work-barometer-hits-all-time-post-pandemic-highs/).

**Datasets**

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
