import React, { useState, useEffect } from "react";
import Papa from "papaparse";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  ResponsiveContainer,
} from "recharts";
import "./App.css";

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#8884d8"];

function App() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAllData();
  }, []);

  const loadAllData = async () => {
    try {
      console.log("Loading all datasets...");

      // Load all three datasets
      const enrollmentData = await loadCSV("/data/enrolment_merged.csv");
      const demographicData = await loadCSV("/data/demographic_merged.csv");
      const biometricData = await loadCSV("/data/biometric_merged.csv");

      console.log("Data loaded!", {
        enrollment: enrollmentData.length,
        demographic: demographicData.length,
        biometric: biometricData.length,
      });

      // Calculate statistics
      const enrollStats = calculateEnrollmentStats(enrollmentData);
      const monthlyTrends = calculateMonthlyTrends(enrollmentData);
      const updateComparison = calculateUpdateComparison(
        demographicData,
        biometricData
      );

      setStats({
        ...enrollStats,
        monthlyTrends,
        updateComparison,
      });
      setLoading(false);
    } catch (error) {
      console.error("Error loading data:", error);
      setLoading(false);
    }
  };

  const loadCSV = (path) => {
    return new Promise((resolve) => {
      Papa.parse(path, {
        download: true,
        header: true,
        dynamicTyping: true,
        complete: (results) => resolve(results.data),
      });
    });
  };

  const calculateEnrollmentStats = (data) => {
    // Top states
    const stateMap = {};
    data.forEach((row) => {
      if (!row.state) return;
      if (!stateMap[row.state]) {
        stateMap[row.state] = { babies: 0, children: 0, adults: 0 };
      }
      stateMap[row.state].babies += row.age_0_5 || 0;
      stateMap[row.state].children += row.age_5_17 || 0;
      stateMap[row.state].adults += row.age_18_greater || 0;
    });

    const topStates = Object.entries(stateMap)
      .map(([state, counts]) => ({
        state,
        total: counts.babies + counts.children + counts.adults,
        babies: counts.babies,
        children: counts.children,
        adults: counts.adults,
      }))
      .sort((a, b) => b.total - a.total)
      .slice(0, 10);

    // Age distribution
    const totalBabies = data.reduce((sum, row) => sum + (row.age_0_5 || 0), 0);
    const totalChildren = data.reduce(
      (sum, row) => sum + (row.age_5_17 || 0),
      0
    );
    const totalAdults = data.reduce(
      (sum, row) => sum + (row.age_18_greater || 0),
      0
    );

    const ageDistribution = [
      { name: "Babies (0-5)", value: totalBabies },
      { name: "Children (5-17)", value: totalChildren },
      { name: "Adults (18+)", value: totalAdults },
    ];

    return {
      topStates,
      ageDistribution,
      totalRecords: data.length,
      totalEnrollments: totalBabies + totalChildren + totalAdults,
    };
  };

  const calculateMonthlyTrends = (data) => {
    const monthMap = {};

    data.forEach((row) => {
      if (!row.date) return;
      const month = row.date.substring(3); // Get "03-2025" from "02-03-2025"

      if (!monthMap[month]) {
        monthMap[month] = { babies: 0, children: 0, adults: 0 };
      }

      monthMap[month].babies += row.age_0_5 || 0;
      monthMap[month].children += row.age_5_17 || 0;
      monthMap[month].adults += row.age_18_greater || 0;
    });

    return Object.entries(monthMap)
      .map(([month, counts]) => ({
        month,
        total: counts.babies + counts.children + counts.adults,
        babies: counts.babies,
        children: counts.children,
        adults: counts.adults,
      }))
      .sort((a, b) => a.month.localeCompare(b.month));
  };

  const calculateUpdateComparison = (demoData, bioData) => {
    // Calculate demographic updates
    const demoChild = demoData.reduce(
      (sum, row) => sum + (row.demo_age_5_17 || 0),
      0
    );
    const demoAdult = demoData.reduce(
      (sum, row) => sum + (row.demo_age_17_ || 0),
      0
    );

    // Calculate biometric updates
    const bioChild = bioData.reduce(
      (sum, row) => sum + (row.bio_age_5_17 || 0),
      0
    );
    const bioAdult = bioData.reduce(
      (sum, row) => sum + (row.bio_age_17_ || 0),
      0
    );

    const updateData = [
      {
        type: "Demographic",
        Children: demoChild,
        Adults: demoAdult,
        total: demoChild + demoAdult,
      },
      {
        type: "Biometric",
        Children: bioChild,
        Adults: bioAdult,
        total: bioChild + bioAdult,
      },
    ];

    // Top states for updates
    const demoStateMap = {};
    demoData.forEach((row) => {
      if (!row.state) return;
      if (!demoStateMap[row.state]) demoStateMap[row.state] = 0;
      demoStateMap[row.state] +=
        (row.demo_age_5_17 || 0) + (row.demo_age_17_ || 0);
    });

    const topDemoStates = Object.entries(demoStateMap)
      .map(([state, total]) => ({ state, updates: total }))
      .sort((a, b) => b.updates - a.updates)
      .slice(0, 5);

    return {
      updateData,
      topDemoStates,
      stats: {
        totalDemo: demoChild + demoAdult,
        totalBio: bioChild + bioAdult,
        demoChildPercent: ((demoChild / (demoChild + demoAdult)) * 100).toFixed(
          1
        ),
        bioChildPercent: ((bioChild / (bioChild + bioAdult)) * 100).toFixed(1),
      },
    };
  };

  if (loading) {
    return (
      <div className="loading">
        <h2>⏳ Loading Aadhaar Data...</h2>
        <p>Processing millions of records...</p>
      </div>
    );
  }

  if (!stats) {
    return <div className="error">Error loading data</div>;
  }

  return (
    <div className="App">
      <header>
        <h1>🇮🇳 Aadhaar Insight Engine</h1>
        <p>Geographic & Temporal Pattern Analysis</p>
      </header>

      <div className="container">
        {/* Overview Cards */}
        <div className="stats-grid">
          <div className="stat-card">
            <h3>📋 Total Records</h3>
            <p className="stat-number">{stats.totalRecords.toLocaleString()}</p>
          </div>
          <div className="stat-card">
            <h3>👥 Total Enrollments</h3>
            <p className="stat-number">
              {stats.totalEnrollments.toLocaleString()}
            </p>
          </div>
          <div className="stat-card">
            <h3>👶 Babies (0-5)</h3>
            <p className="stat-number">
              {stats.ageDistribution[0].value.toLocaleString()}
            </p>
          </div>
          <div className="stat-card">
            <h3>🎓 Children (5-17)</h3>
            <p className="stat-number">
              {stats.ageDistribution[1].value.toLocaleString()}
            </p>
          </div>
        </div>

        {/* Top States Chart */}
        <div className="chart-container">
          <h2>📍 Top 10 States - Enrollment</h2>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={stats.topStates}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="state"
                angle={-45}
                textAnchor="end"
                height={100}
              />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar
                dataKey="babies"
                stackId="a"
                fill="#FF6B6B"
                name="Babies (0-5)"
              />
              <Bar
                dataKey="children"
                stackId="a"
                fill="#4ECDC4"
                name="Children (5-17)"
              />
              <Bar
                dataKey="adults"
                stackId="a"
                fill="#45B7D1"
                name="Adults (18+)"
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Age Distribution Pie Chart */}
        <div className="chart-container">
          <h2>👶 Age Group Distribution</h2>
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={stats.ageDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) =>
                  `${name}: ${(percent * 100).toFixed(1)}%`
                }
                outerRadius={120}
                fill="#8884d8"
                dataKey="value"
              >
                {stats.ageDistribution.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Monthly Trends Chart */}
        <div className="chart-container">
          <h2>📅 Monthly Enrollment Trends</h2>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={stats.monthlyTrends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="total"
                stroke="#8884d8"
                strokeWidth={3}
                name="Total Enrollments"
              />
              <Line
                type="monotone"
                dataKey="babies"
                stroke="#FF6B6B"
                name="Babies (0-5)"
              />
              <Line
                type="monotone"
                dataKey="children"
                stroke="#4ECDC4"
                name="Children (5-17)"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Update Comparison Analysis */}
        <div className="chart-container">
          <h2>🔄 Update Behavior Analysis - Demographic vs Biometric</h2>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={stats.updateComparison.updateData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="type" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="Children" fill="#4ECDC4" name="Children (5-17)" />
              <Bar dataKey="Adults" fill="#FF6B6B" name="Adults (17+)" />
            </BarChart>
          </ResponsiveContainer>

          <div className="update-stats">
            <div className="update-stat-box">
              <h3>📝 Demographic Updates</h3>
              <p className="big-number">
                {stats.updateComparison.stats.totalDemo.toLocaleString()}
              </p>
              <p>
                Children: {stats.updateComparison.stats.demoChildPercent}% |
                Adults:{" "}
                {(100 - stats.updateComparison.stats.demoChildPercent).toFixed(
                  1
                )}
                %
              </p>
            </div>
            <div className="update-stat-box">
              <h3>👁️ Biometric Updates</h3>
              <p className="big-number">
                {stats.updateComparison.stats.totalBio.toLocaleString()}
              </p>
              <p>
                Children: {stats.updateComparison.stats.bioChildPercent}% |
                Adults:{" "}
                {(100 - stats.updateComparison.stats.bioChildPercent).toFixed(
                  1
                )}
                %
              </p>
            </div>
            <div className="update-stat-box highlight">
              <h3>💡 Key Finding</h3>
              <p className="insight-text">
                Biometric updates are{" "}
                <strong>
                  {(
                    stats.updateComparison.stats.totalBio /
                    stats.updateComparison.stats.totalDemo
                  ).toFixed(2)}
                  x
                </strong>{" "}
                more common than demographic updates!
              </p>
              <p className="insight-text">
                Adults dominate demographic updates (90%), but biometric updates
                are almost equal (51% adults vs 49% children)
              </p>
            </div>
          </div>
        </div>

        {/* Key Insights */}
        <div className="insights-container">
          <h2>💡 Key Insights</h2>
          <div className="insights-grid">
            <div className="insight-card">
              <h3>🏆 Top State</h3>
              <p className="insight-text">
                Uttar Pradesh leads with <strong>1+ million</strong> enrollments
              </p>
            </div>
            <div className="insight-card">
              <h3>👶 Baby Boom</h3>
              <p className="insight-text">
                <strong>65.3%</strong> enrollments are babies (0-5 years)
              </p>
            </div>
            <div className="insight-card">
              <h3>📈 Peak Month</h3>
              <p className="insight-text">
                September 2025 saw <strong>1.5 million</strong> enrollments
              </p>
            </div>
            <div className="insight-card">
              <h3>🎯 Coverage</h3>
              <p className="insight-text">
                Only <strong>3.1%</strong> adult enrollments - most already have
                Aadhaar
              </p>
            </div>
          </div>
        </div>

        {/* Actionable Recommendations */}
        <div className="recommendations-container">
          <h2>🎯 Strategic Recommendations for UIDAI</h2>
          <p className="recommendations-intro">
            Based on comprehensive analysis of 4.5+ million records, here are
            data-driven recommendations:
          </p>

          <div className="recommendations-grid">
            <div className="recommendation-card priority-high">
              <div className="priority-badge">HIGH PRIORITY</div>
              <h3>🚀 Leverage September Momentum</h3>
              <p>
                <strong>Finding:</strong> September 2025 saw 1.5M enrollments
                (2x normal)
              </p>
              <p>
                <strong>Action:</strong> Investigate what caused the spike
                (back-to-school campaigns?) and replicate the strategy in other
                months
              </p>
              <p>
                <strong>Impact:</strong> Could double annual enrollment rates
              </p>
            </div>

            <div className="recommendation-card priority-high">
              <div className="priority-badge">HIGH PRIORITY</div>
              <h3>👶 Focus on Baby Enrollment</h3>
              <p>
                <strong>Finding:</strong> 65.3% enrollments are babies (0-5
                years)
              </p>
              <p>
                <strong>Action:</strong> Partner with hospitals and maternity
                centers for birth-time Aadhaar enrollment
              </p>
              <p>
                <strong>Impact:</strong> Near 100% coverage for newborns
              </p>
            </div>

            <div className="recommendation-card priority-medium">
              <div className="priority-badge">MEDIUM PRIORITY</div>
              <h3>🔄 Optimize Update Services</h3>
              <p>
                <strong>Finding:</strong> Biometric updates (64M) exceed
                demographic updates (48M)
              </p>
              <p>
                <strong>Action:</strong> Expand biometric update centers,
                especially in high-demand states (UP, Bihar, Maharashtra)
              </p>
              <p>
                <strong>Impact:</strong> Reduce wait times and improve service
                quality
              </p>
            </div>

            <div className="recommendation-card priority-medium">
              <div className="priority-badge">MEDIUM PRIORITY</div>
              <h3>🎓 Target School-Age Children</h3>
              <p>
                <strong>Finding:</strong> 31.6% enrollments are children (5-17),
                but biometric updates show 49% are children
              </p>
              <p>
                <strong>Action:</strong> Children's biometrics change as they
                grow - implement automatic update reminders at ages 5, 10, and
                15
              </p>
              <p>
                <strong>Impact:</strong> Maintain accurate biometric data for
                all children
              </p>
            </div>

            <div className="recommendation-card priority-low">
              <div className="priority-badge">LOW PRIORITY</div>
              <h3>📍 District-Level Campaigns</h3>
              <p>
                <strong>Finding:</strong> Top districts (Thane, Sitamarhi,
                Bahraich) show concentrated activity
              </p>
              <p>
                <strong>Action:</strong> Share best practices from
                high-performing districts with underperforming ones
              </p>
              <p>
                <strong>Impact:</strong> Balanced nationwide coverage
              </p>
            </div>

            <div className="recommendation-card priority-low">
              <div className="priority-badge">INSIGHT</div>
              <h3>📊 Adult Coverage Analysis</h3>
              <p>
                <strong>Finding:</strong> Only 3.1% enrollments are adults -
                most already have Aadhaar
              </p>
              <p>
                <strong>Insight:</strong> Focus should shift from new adult
                enrollments to service quality and updates
              </p>
              <p>
                <strong>Impact:</strong> Better resource allocation
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
