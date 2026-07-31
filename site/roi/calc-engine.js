// ============================================================
//  CALC ENGINE — faithful port of the Excel model
//  "Sabato AI vs Human Operator in Italy"
//  All three sheets reduced to one compute() function.
// ============================================================

const DEFAULTS = {
  // --- Scenario ---
  numOperators: 5,         // size of the team you'd replace
  callVolume: 1000,        // monthly calls PER operator
  callDuration: 5,         // avg minutes per call

  // --- Human: salary basis (RAL) ---
  ral: 29000,              // gross annual salary
  inpsRate: 0.30,          // INPS employer contributions
  tfrRate: 0.0691,         // TFR severance accrual
  inailRate: 0.005,        // INAIL accident insurance

  // --- Human: working-days deductions (out of 365) ---
  weekends: 104,
  holidays: 11,
  ferie: 26,               // annual leave
  rol: 8,                  // permessi retribuiti
  sick: 9,
  training: 3,
  closures: 3,             // ferragosto / company closures

  // --- Human: phone-time deductions (out of shift) ---
  shift: 8,
  lunch: 1,
  coffee: 0.5,
  email: 0.75,
  crm: 1.5,
  meetings: 0.25,

  // --- Human: other annual costs ---
  recruitment: 2000,
  trainingCost: 1500,

  // --- Sabato pricing ---
  sabatoCPM: 0.50,         // cost per minute
  sabatoMonthlyFee: 0,     // platform fee / month
  sabatoSetup: 0,          // one-time implementation

  // --- 24/7 scenario ---
  agents247: 5,            // human agents needed for round-the-clock
};

function compute(i) {
  // ---------- 1. Employer costs on top of RAL ----------
  const inps = i.ral * i.inpsRate;
  const tfr = i.ral * i.tfrRate;
  const inail = i.ral * i.inailRate;
  const quattordicesima = i.ral / 13;            // 14th month (Excel uses RAL/13)
  const employerAddon = inps + tfr + inail + quattordicesima;
  const employerPct = employerAddon / i.ral;

  // ---------- 2. Costo Azienda (all-in employment cost) ----------
  const costoAzienda = i.ral + employerAddon;
  const costoAziendaMonth = costoAzienda / 12;

  // ---------- 3. Actual working days ----------
  const calendarDays = 365;
  const daysWorked = calendarDays - i.weekends - i.holidays - i.ferie
                     - i.rol - i.sick - i.training - i.closures;
  const paidNonWorking = calendarDays - i.weekends - daysWorked; // paid, zero output

  // ---------- 4. Productive phone minutes per day ----------
  const phoneHours = i.shift - i.lunch - i.coffee - i.email - i.crm - i.meetings;
  const phoneMinPerDay = phoneHours * 60;
  const utilization = phoneHours / i.shift;

  // ---------- 5. The real per-minute number ----------
  const productiveMinYear = daysWorked * phoneMinPerDay;
  const humanCPM = costoAzienda / productiveMinYear;     // cost per PRODUCTIVE minute
  const humanCostPerHour = humanCPM * 60;
  const callsPerDay = phoneMinPerDay / i.callDuration;
  const callsPerYear = callsPerDay * daysWorked;

  // ---------- 6. Annual comparison (1 agent, business hours) ----------
  const totalMinMonth = i.callVolume * i.callDuration;

  // Human all-in annual
  const turnover = i.recruitment / 3;                    // replace every 18mo
  const humanAnnual = costoAzienda + i.recruitment + i.trainingCost + turnover;
  const humanMonthly = humanAnnual / 12;

  // Sabato annual
  const sabatoPlatformAnnual = i.sabatoMonthlyFee * 12;
  const sabatoUsage = totalMinMonth * 12 * i.sabatoCPM;
  const sabatoAnnual = i.sabatoSetup + sabatoPlatformAnnual + sabatoUsage;
  const sabatoMonthly = sabatoAnnual / 12;

  const annualSavings = humanAnnual - sabatoAnnual;
  const monthlySavings = humanMonthly - sabatoMonthly;
  const savingsPct = humanAnnual > 0 ? annualSavings / humanAnnual : 0;

  // ---------- Unit economics ----------
  const cpmSavings = humanCPM - i.sabatoCPM;
  const pctCheaper = humanCPM > 0 ? 1 - (i.sabatoCPM / humanCPM) : 0;
  const humanCostPerCall = humanCPM * i.callDuration;
  const sabatoCostPerCall = i.sabatoCPM * i.callDuration;

  // ---------- Coverage ----------
  const humanCoverageHoursDay = i.shift;
  const humanCoverageDaysYear = daysWorked;
  const humanCoverageHoursYear = humanCoverageHoursDay * humanCoverageDaysYear;
  const sabatoCoverageHoursDay = 24;
  const sabatoCoverageDaysYear = 365;
  const sabatoCoverageHoursYear = 24 * 365;

  // ---------- 24/7 scenario ----------
  // ---------- Replace-your-team scenario (business hours) ----------
  const numOperators = i.numOperators;
  const fleetHumanAnnual = numOperators * humanAnnual;
  const fleetHumanMonthly = fleetHumanAnnual / 12;
  const fleetSabatoUsage = numOperators * sabatoUsage;
  const fleetSabatoAnnual = i.sabatoSetup + sabatoPlatformAnnual + fleetSabatoUsage;
  const fleetSabatoMonthly = fleetSabatoAnnual / 12;
  const fleetSavings = fleetHumanAnnual - fleetSabatoAnnual;
  const fleetSavingsMonthly = fleetHumanMonthly - fleetSabatoMonthly;
  const fleetSavingsPct = fleetHumanAnnual > 0 ? fleetSavings / fleetHumanAnnual : 0;
  const fleetCallsMonth = numOperators * i.callVolume;
  const fleetMinMonth = numOperators * totalMinMonth;

  // ---------- 24/7 scenario ----------
  const human247Annual = i.agents247 * costoAzienda;     // Excel: agents × Costo Azienda
  const human247Monthly = human247Annual / 12;
  const sabato247Annual = sabatoAnnual;
  const sabato247Monthly = sabatoMonthly;
  const savings247 = human247Annual - sabato247Annual;

  return {
    inps, tfr, inail, quattordicesima, employerAddon, employerPct,
    costoAzienda, costoAziendaMonth,
    calendarDays, daysWorked, paidNonWorking,
    phoneHours, phoneMinPerDay, utilization,
    productiveMinYear, humanCPM, humanCostPerHour, callsPerDay, callsPerYear,
    totalMinMonth,
    turnover, humanAnnual, humanMonthly,
    sabatoPlatformAnnual, sabatoUsage, sabatoAnnual, sabatoMonthly,
    annualSavings, monthlySavings, savingsPct,
    cpmSavings, pctCheaper, humanCostPerCall, sabatoCostPerCall,
    humanCoverageHoursDay, humanCoverageDaysYear, humanCoverageHoursYear,
    sabatoCoverageHoursDay, sabatoCoverageDaysYear, sabatoCoverageHoursYear,
    human247Annual, human247Monthly, sabato247Annual, sabato247Monthly, savings247,
    fleetHumanAnnual, fleetHumanMonthly, fleetSabatoAnnual, fleetSabatoMonthly,
    fleetSavings, fleetSavingsMonthly, fleetSavingsPct, fleetCallsMonth, fleetMinMonth,
  };
}

// ============================================================
//  FORMAT HELPERS — locale-aware (en / it)
// ============================================================
function makeFmt(lang) {
  const loc = lang === 'it' ? 'it-IT' : 'en-IE';
  const dec = lang === 'it' ? ',' : '.';
  const eur = new Intl.NumberFormat(loc, { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
  const eur2 = new Intl.NumberFormat(loc, { style: 'currency', currency: 'EUR', minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const num = new Intl.NumberFormat(loc, { maximumFractionDigits: 0 });
  return {
    eur:  (n) => eur.format(Math.round(n)),
    eur2: (n) => eur2.format(n),
    cpm:  (n) => '€' + n.toFixed(3).replace('.', dec),   // per-minute, 3 decimals
    num:  (n) => num.format(Math.round(n)),
    pct:  (n, d = 0) => (n * 100).toFixed(d).replace('.', dec) + '%',
    hours:(n) => (Number.isInteger(n) ? n : n.toFixed(2).replace('.', dec)) + 'h',
  };
}

Object.assign(window, { compute, DEFAULTS, makeFmt });
