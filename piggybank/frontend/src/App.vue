<template>
  <div class="min-h-screen bg-[#f8fafc] dark:bg-slate-950 text-slate-900 dark:text-slate-100 font-sans transition-colors duration-300">
    <!-- Navigation / Header -->
    <header class="sticky top-0 z-40 w-full backdrop-blur flex-none transition-colors duration-500 lg:z-50 lg:border-b lg:border-slate-900/10 dark:border-slate-50/[0.06] bg-white/75 dark:bg-slate-900/75">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-indigo-600 rounded-lg shadow-lg shadow-indigo-500/30">
              <BanknotesIcon class="w-6 h-6 text-white" />
            </div>
            <h1 class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-violet-600 dark:from-indigo-400 dark:to-violet-400">
              Piggybank Dashboard
            </h1>
          </div>
          
          <div class="flex items-center gap-4">
            <button @click="exportData" class="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700 transition-all active:scale-95" title="Daten exportieren">
              <ArrowDownTrayIcon class="w-5 h-5" />
            </button>
            <label class="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700 transition-all active:scale-95 cursor-pointer" title="Daten importieren">
              <ArrowUpTrayIcon class="w-5 h-5" />
              <input type="file" @change="importData" class="hidden" accept=".json" />
            </label>
            <button @click="toggleDarkMode" class="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700 transition-all active:scale-95">
              <SunIcon v-if="isDark" class="w-5 h-5" />
              <MoonIcon v-else class="w-5 h-5" />
            </button>
            <button @click="showAddPersonModal = true" class="hidden sm:flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-xl font-medium shadow-lg shadow-indigo-600/20 transition-all active:scale-95">
              <PlusIcon class="w-5 h-5" />
              Person hinzufügen
            </button>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      <!-- Notifications (Toasts) -->
      <div class="fixed top-20 right-4 z-50 flex flex-col gap-2 pointer-events-none">
        <TransitionGroup name="toast">
          <div v-if="error" key="error" class="pointer-events-auto bg-white dark:bg-slate-800 border-l-4 border-rose-500 shadow-xl rounded-lg p-4 flex items-start gap-3 min-w-[300px] animate-in slide-in-from-right">
            <XCircleIcon class="w-6 h-6 text-rose-500 shrink-0" />
            <div class="flex-1">
              <p class="font-bold text-slate-900 dark:text-white">Fehler</p>
              <p class="text-sm text-slate-500 dark:text-slate-400">{{ error }}</p>
            </div>
            <button @click="error = ''" class="text-slate-400 hover:text-slate-600">
              <XMarkIcon class="w-5 h-5" />
            </button>
          </div>
          <div v-if="success" key="success" class="pointer-events-auto bg-white dark:bg-slate-800 border-l-4 border-emerald-500 shadow-xl rounded-lg p-4 flex items-start gap-3 min-w-[300px] animate-in slide-in-from-right">
            <CheckCircleIcon class="w-6 h-6 text-emerald-500 shrink-0" />
            <div class="flex-1">
              <p class="font-bold text-slate-900 dark:text-white">Erfolg</p>
              <p class="text-sm text-slate-500 dark:text-slate-400">{{ success }}</p>
            </div>
            <button @click="success = ''" class="text-slate-400 hover:text-slate-600">
              <XMarkIcon class="w-5 h-5" />
            </button>
          </div>
        </TransitionGroup>
      </div>

      <div v-if="loading" class="flex flex-col justify-center items-center h-[60vh] gap-4">
        <div class="relative w-16 h-16">
          <div class="absolute inset-0 rounded-full border-4 border-indigo-200 dark:border-indigo-900"></div>
          <div class="absolute inset-0 rounded-full border-4 border-indigo-600 border-t-transparent animate-spin"></div>
        </div>
        <p class="text-slate-500 animate-pulse">Lade deine Piggybanks...</p>
      </div>
      
      <div v-else>
        <!-- Navigation Tabs -->
        <div class="flex gap-2 mb-8 bg-slate-100 dark:bg-slate-800 p-1.5 rounded-2xl">
          <button @click="activeTab = 'dashboard'" 
                  class="flex-1 py-3 px-4 rounded-xl font-bold text-sm transition-all"
                  :class="activeTab === 'dashboard' ? 'bg-white dark:bg-slate-700 shadow text-indigo-600 dark:text-indigo-400' : 'text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'">
            <BanknotesIcon class="w-5 h-5 inline mr-2" />
            Dashboard
          </button>
          <button @click="activeTab = 'recurring'" 
                  class="flex-1 py-3 px-4 rounded-xl font-bold text-sm transition-all"
                  :class="activeTab === 'recurring' ? 'bg-white dark:bg-slate-700 shadow text-indigo-600 dark:text-indigo-400' : 'text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'">
            <ArrowPathIcon class="w-5 h-5 inline mr-2" />
            Abos
          </button>
          <button @click="activeTab = 'yearly'" 
                  class="flex-1 py-3 px-4 rounded-xl font-bold text-sm transition-all"
                  :class="activeTab === 'yearly' ? 'bg-white dark:bg-slate-700 shadow text-indigo-600 dark:text-indigo-400' : 'text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'">
            <CalendarIcon class="w-5 h-5 inline mr-2" />
            Jahresübersicht
          </button>
        </div>

        <!-- Dashboard Tab -->
        <div v-if="activeTab === 'dashboard'">
        <!-- Section Header -->
        <div class="flex justify-between items-end mb-6">
          <div>
            <h2 class="text-2xl font-black tracking-tight">Deine Konten</h2>
            <p class="text-slate-500">Übersicht aller Familienmitglieder</p>
          </div>
          <button @click="showAddPersonModal = true" class="sm:hidden p-2 bg-indigo-600 text-white rounded-lg shadow-lg">
            <PlusIcon class="w-6 h-6" />
          </button>
        </div>

        <!-- Empty State -->
        <div v-if="persons.length === 0" class="bg-white dark:bg-slate-800 rounded-3xl p-12 text-center border-2 border-dashed border-slate-200 dark:border-slate-700 flex flex-col items-center gap-6">
          <div class="w-32 h-32 bg-indigo-50 dark:bg-indigo-900/20 rounded-full flex items-center justify-center">
            <UserGroupIcon class="w-16 h-16 text-indigo-200 dark:text-indigo-800" />
          </div>
          <div class="max-w-md">
            <h3 class="text-xl font-bold mb-2">Willkommen bei Piggybank!</h3>
            <p class="text-slate-500 mb-8">Es wurden noch keine Konten angelegt. Beginne damit, für jedes Familienmitglied ein Profil zu erstellen, um das Taschengeld zu tracken.</p>
            <button @click="showAddPersonModal = true" class="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 rounded-2xl font-bold shadow-xl shadow-indigo-600/30 transition-all hover:-translate-y-1 active:scale-95">
              <PlusIcon class="w-6 h-6" />
              Erstes Konto erstellen
            </button>
          </div>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          <div v-for="person in persons" :key="person.id" 
               @click="toggleAccountFilter(person.id)"
               class="bg-white dark:bg-slate-900 rounded-3xl shadow-sm hover:shadow-xl border-2 overflow-hidden transition-all duration-300 flex flex-col group cursor-pointer"
               :class="selectedAccountId === person.id ? 'border-indigo-500 ring-4 ring-indigo-500/20' : 'border-slate-200 dark:border-slate-800'">
            <div class="p-8 pb-4">
              <div class="flex justify-between items-start mb-6">
                <div class="relative">
                  <div class="h-16 w-16 rounded-2xl bg-gradient-to-br from-indigo-100 to-indigo-50 dark:from-indigo-900/40 dark:to-indigo-800/20 flex items-center justify-center shadow-inner group-hover:scale-110 transition-transform">
                    <span class="text-2xl font-black text-indigo-600 dark:text-indigo-400">{{ person.name.charAt(0).toUpperCase() }}</span>
                  </div>
                  <div class="absolute -bottom-1 -right-1 w-6 h-6 bg-emerald-500 border-4 border-white dark:border-slate-800 rounded-full"></div>
                </div>
                <div class="flex gap-1">
                  <button @click.stop.prevent="viewDetails(person)" class="p-2 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 dark:hover:bg-indigo-900/50 rounded-lg transition" title="Verlauf anzeigen">
                    <ChartBarIcon class="w-5 h-5" />
                  </button>
                  <button @click.stop.prevent="confirmDeletePerson(person)" class="relative z-10 p-2 text-slate-400 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-900/50 rounded-lg transition" title="Konto löschen">
                    <TrashIcon class="w-5 h-5 px-0.5" />
                  </button>
                </div>
              </div>
              
              <h2 class="text-2xl font-black mb-1 truncate">{{ person.name }}</h2>
              <div class="inline-flex items-baseline gap-1 py-1 px-4 rounded-xl mb-6" :class="person.balance >= 0 ? 'bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600' : 'bg-rose-50 dark:bg-rose-900/20 text-rose-600'">
                <span class="text-3xl font-black">{{ person.balance.toFixed(2) }}</span>
                <span class="text-lg font-bold">€</span>
              </div>

              <!-- Individual Account Stats (Point 4) -->
              <div class="grid grid-cols-2 gap-3 pt-4 border-t border-slate-100 dark:border-slate-800">
                <div class="flex flex-col">
                  <span class="text-[10px] font-black uppercase text-slate-400 tracking-wider">Einnahmen (Monat)</span>
                  <span class="text-emerald-500 font-bold text-sm">+{{ getPersonStats(person.id).income.toFixed(2) }} €</span>
                </div>
                <div class="flex flex-col">
                  <span class="text-[10px] font-black uppercase text-slate-400 tracking-wider">Ausgaben (Monat)</span>
                  <span class="text-rose-500 font-bold text-sm">{{ getPersonStats(person.id).expense.toFixed(2) }} €</span>
                </div>
              </div>
            </div>
            
            <div class="mt-auto px-8 py-6 bg-slate-50/50 dark:bg-slate-900/20 border-t border-slate-200 dark:border-slate-700/50 grid grid-cols-2 gap-4">
              <button @click="openTxModal(person, 'income')" class="flex items-center justify-center gap-2 py-3 px-4 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold shadow-lg shadow-emerald-500/20 transition-all active:scale-95 text-sm">
                <PlusIcon class="w-4 h-4" />
                Sparen
              </button>
              <button @click="openTxModal(person, 'expense')" class="flex items-center justify-center gap-2 py-3 px-4 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-800 hover:border-rose-500 dark:hover:border-rose-400 hover:text-rose-600 text-slate-600 dark:text-slate-200 rounded-xl font-bold transition-all active:scale-95 text-sm">
                <MinusIcon class="w-4 h-4" />
                Ausgeben
              </button>
            </div>
          </div>
        </div>

        <!-- Chart Detail View -->
        <Transition name="fade">
          <div v-if="activeChartView" class="bg-white dark:bg-slate-800 rounded-3xl shadow-xl border border-slate-200 dark:border-slate-700/50 p-8 mb-12 animate-in fade-in zoom-in duration-300">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
              <div>
                <h3 class="text-2xl font-black flex items-center gap-3">
                  <ChartBarIcon class="w-8 h-8 text-indigo-500" />
                  Verlauf: {{ activeChartView.name }}
                </h3>
                <p class="text-slate-500">Saldo-Entwicklung der letzten Transaktionen</p>
              </div>
              <button @click="activeChartView = null" class="px-4 py-2 bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600 rounded-xl font-bold transition">Schließen</button>
            </div>
            
            <div class="bg-slate-50 dark:bg-slate-900/50 rounded-2xl p-4 sm:p-6 lg:p-8">
              <div v-if="chartData" class="h-80 sm:h-96 w-full">
                  <Line :data="chartData" :options="chartOptions" />
              </div>
              <div v-else class="flex flex-col items-center justify-center py-20 text-slate-400 gap-4">
                  <ClockIcon class="w-12 h-12 opacity-20" />
                  <p>Noch nicht genug Buchungen für eine Analyse vorhanden.</p>
              </div>
            </div>
          </div>
        </Transition>

        <!-- (Point 3) Historie & Suche -->
        <div class="mt-16 bg-white dark:bg-slate-800 rounded-3xl shadow-sm border border-slate-200 dark:border-slate-700/50 overflow-hidden mb-20 animate-in fade-in slide-in-from-bottom duration-700">
          <div class="p-8 border-b border-slate-200 dark:border-slate-700/50">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div>
                <h3 class="text-2xl font-black flex items-center gap-3">
                  <ClockIcon class="w-7 h-7 text-indigo-500" />
                  Historie & Analyse
                </h3>
                <p class="text-slate-500">Durchsuche alle Buchungen und filtere nach Zeitraum</p>
              </div>
              
              <div class="flex flex-wrap items-center gap-4">
                <div class="relative">
                  <MagnifyingGlassIcon class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                  <input type="text" v-model="searchQuery" placeholder="Suche..." 
                         class="pl-10 pr-4 py-2 bg-slate-50 dark:bg-slate-900/50 border border-slate-100 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-sm w-full sm:w-64" />
                </div>
                <div class="flex items-center gap-2">
                  <input type="date" v-model="filterDateFrom" class="bg-slate-50 dark:bg-slate-900/50 border border-slate-100 dark:border-slate-700 rounded-xl px-3 py-2 text-xs outline-none focus:ring-2 focus:ring-indigo-500" />
                  <span class="text-slate-400">bis</span>
                  <input type="date" v-model="filterDateTo" class="bg-slate-50 dark:bg-slate-900/50 border border-slate-100 dark:border-slate-700 rounded-xl px-3 py-2 text-xs outline-none focus:ring-2 focus:ring-indigo-500" />
                </div>
              </div>
            </div>
          </div>
          
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-slate-200 dark:divide-slate-700/50 text-left">
              <thead>
                <tr class="bg-slate-50/50 dark:bg-slate-900/30">
                  <th class="px-8 py-4 text-xs font-bold text-slate-400 uppercase tracking-widest">Datum</th>
                  <th class="px-8 py-4 text-xs font-bold text-slate-400 uppercase tracking-widest">Konto</th>
                  <th class="px-8 py-4 text-xs font-bold text-slate-400 uppercase tracking-widest">Zweck</th>
                  <th class="px-8 py-4 text-xs font-bold text-slate-400 uppercase tracking-widest text-right">Betrag</th>
                  <th class="px-8 py-4 text-xs font-bold text-slate-400 uppercase tracking-widest text-center">Aktion</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 dark:divide-slate-700/30">
                <tr v-for="tx in historyTransactions" :key="tx.id" 
                    class="hover:bg-slate-50 dark:hover:bg-slate-700/20 transition-colors group">
                  <td class="px-8 py-4 whitespace-nowrap text-sm text-slate-500 font-medium cursor-pointer" @click="openEditTxModal(tx)">{{ formatDate(tx.date) }}</td>
                  <td class="px-8 py-4 cursor-pointer" @click="openEditTxModal(tx)">
                    <span class="inline-flex items-center gap-2 font-bold text-sm">
                       {{ getPersonName(tx.person_id) }}
                    </span>
                  </td>
                  <td class="px-8 py-4 text-sm text-slate-600 dark:text-slate-400 cursor-pointer" @click="openEditTxModal(tx)">
                    <span class="group-hover:text-indigo-500 transition-colors">"{{ tx.note || '-' }}"</span>
                    <PencilIcon class="w-3 h-3 inline ml-1 opacity-0 group-hover:opacity-50 transition-opacity" />
                  </td>
                  <td class="px-8 py-4 whitespace-nowrap text-right font-black cursor-pointer" :class="tx.amount > 0 ? 'text-emerald-500' : 'text-rose-500'" @click="openEditTxModal(tx)">
                    {{ tx.amount > 0 ? '+' : '' }}{{ tx.amount.toFixed(2) }} €
                  </td>
                  <td class="px-8 py-4 text-center">
                    <button @click.stop="confirmDeleteTransaction(tx)" class="p-2 text-slate-400 hover:text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-900/30 rounded-lg transition opacity-0 group-hover:opacity-100" title="Buchung löschen">
                      <TrashIcon class="w-4 h-4" />
                    </button>
                  </td>
                </tr>
                <tr v-if="historyTransactions.length === 0">
                  <td colspan="5" class="px-8 py-10 text-center text-slate-400 italic text-sm">Keine Einträge für diese Suche gefunden.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        </div> <!-- End Dashboard Tab -->

        <!-- Recurring Transactions Tab -->
        <div v-if="activeTab === 'recurring'" class="animate-in fade-in duration-300">
          <div class="flex justify-between items-end mb-6">
            <div>
              <h2 class="text-2xl font-black tracking-tight">Abonnements & Abos</h2>
              <p class="text-slate-500">Verwalte wiederkehrende Ausgaben</p>
            </div>
            <button @click="showAddRecurringModal = true" class="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-xl font-medium shadow-lg shadow-indigo-600/20 transition-all active:scale-95">
              <PlusIcon class="w-5 h-5" />
              Neues Abo
            </button>
          </div>

          <div v-if="recurringTransactions.length === 0" class="bg-white dark:bg-slate-800 rounded-3xl p-12 text-center border-2 border-dashed border-slate-200 dark:border-slate-700">
            <ArrowPathIcon class="w-16 h-16 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
            <h3 class="text-xl font-bold mb-2">Keine Abos vorhanden</h3>
            <p class="text-slate-500">Erstelle ein Abo für wiederkehrende Ausgaben wie Fitnessstudio, Streaming-Dienste, etc.</p>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="rt in recurringTransactions" :key="rt.id" 
                 class="bg-white dark:bg-slate-800 rounded-2xl p-6 border border-slate-200 dark:border-slate-700 hover:shadow-lg transition-all">
              <div class="flex justify-between items-start mb-4">
                <div class="flex items-center gap-3">
                  <div class="p-3 rounded-xl" :class="rt.amount < 0 ? 'bg-rose-50 dark:bg-rose-900/30 text-rose-500' : 'bg-emerald-50 dark:bg-emerald-900/30 text-emerald-500'">
                    <ArrowPathIcon class="w-6 h-6" />
                  </div>
                  <div>
                    <h3 class="font-bold text-lg">{{ rt.note || 'Ohne Notiz' }}</h3>
                    <p class="text-sm text-slate-500">{{ getPersonName(rt.person_id) }}</p>
                  </div>
                </div>
                <div class="flex gap-1">
                  <button @click="openEditRecurringModal(rt)" class="p-2 text-slate-400 hover:text-indigo-500 hover:bg-indigo-50 dark:hover:bg-indigo-900/30 rounded-lg transition">
                    <PencilIcon class="w-4 h-4" />
                  </button>
                  <button @click="confirmDeleteRecurring(rt)" class="p-2 text-slate-400 hover:text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-900/30 rounded-lg transition">
                    <TrashIcon class="w-4 h-4" />
                  </button>
                </div>
              </div>
              
              <div class="flex justify-between items-center pt-4 border-t border-slate-100 dark:border-slate-700">
                <div>
                  <span class="text-2xl font-black" :class="rt.amount < 0 ? 'text-rose-500' : 'text-emerald-500'">
                    {{ rt.amount > 0 ? '+' : '' }}{{ rt.amount.toFixed(2) }} €
                  </span>
                  <span class="text-sm text-slate-500 ml-2">{{ getIntervalLabel(rt.interval) }}</span>
                </div>
                <div class="text-right">
                  <span class="text-xs text-slate-400">Nächste Buchung</span>
                  <p class="text-sm font-bold">{{ formatDate(rt.next_execution) }}</p>
                </div>
              </div>
              
              <div class="mt-4 flex items-center gap-2">
                <span class="text-xs px-2 py-1 rounded-full" :class="rt.active ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600' : 'bg-slate-100 dark:bg-slate-700 text-slate-500'">
                  {{ rt.active ? 'Aktiv' : 'Pausiert' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Yearly Overview Tab -->
        <div v-if="activeTab === 'yearly'" class="animate-in fade-in duration-300">
          <div class="flex justify-between items-end mb-6">
            <div>
              <h2 class="text-2xl font-black tracking-tight">Jahresübersicht {{ currentYear }}</h2>
              <p class="text-slate-500">Voraussichtliche Entwicklung der Konten</p>
            </div>
            <div class="flex gap-2">
              <button @click="currentYear--" class="p-2 bg-slate-100 dark:bg-slate-800 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition">
                <ChevronLeftIcon class="w-5 h-5" />
              </button>
              <button @click="currentYear++" class="p-2 bg-slate-100 dark:bg-slate-800 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition">
                <ChevronRightIcon class="w-5 h-5" />
              </button>
            </div>
          </div>

          <div class="bg-white dark:bg-slate-800 rounded-3xl p-6 border border-slate-200 dark:border-slate-700 overflow-x-auto">
            <table class="min-w-full">
              <thead>
                <tr class="border-b border-slate-200 dark:border-slate-700">
                  <th class="py-3 px-4 text-left text-xs font-bold text-slate-400 uppercase">Konto</th>
                  <th v-for="month in monthNames" :key="month" class="py-3 px-2 text-center text-xs font-bold text-slate-400 uppercase">{{ month }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="person in persons" :key="person.id" class="border-b border-slate-100 dark:border-slate-700/50">
                  <td class="py-4 px-4 font-bold">{{ person.name }}</td>
                  <td v-for="(month, idx) in monthNames" :key="month" class="py-4 px-2 text-center">
                    <div class="text-sm font-black" :class="getYearlyProjection(person.id, idx).balance >= 0 ? 'text-emerald-500' : 'text-rose-500'">
                      {{ getYearlyProjection(person.id, idx).balance.toFixed(0) }} €
                    </div>
                    <div class="text-[10px] text-slate-400">
                      <span v-if="getYearlyProjection(person.id, idx).income > 0" class="text-emerald-400">+{{ getYearlyProjection(person.id, idx).income.toFixed(0) }}</span>
                      <span v-if="getYearlyProjection(person.id, idx).expense > 0" class="text-rose-400"> -{{ getYearlyProjection(person.id, idx).expense.toFixed(0) }}</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div class="mt-6 p-4 bg-indigo-50 dark:bg-indigo-900/20 rounded-2xl">
            <p class="text-sm text-indigo-600 dark:text-indigo-400">
              <strong>Hinweis:</strong> Die Prognose basiert auf den bisherigen Durchschnittswerten und den geplanten Abonnements. 
              Tatsächliche Werte können abweichen.
            </p>
          </div>
        </div>

      </div>
    </main>

    <!-- Modal: Add Person -->
    <Transition name="modal">
      <div v-if="showAddPersonModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-slate-900/80 backdrop-blur-md" @click="showAddPersonModal = false"></div>
        
        <!-- Modal Content -->
        <div class="relative bg-white dark:bg-slate-800 rounded-[2.5rem] shadow-2xl w-full max-w-md border border-slate-200 dark:border-slate-700 overflow-visible transition-all duration-300">
          <div class="p-8 sm:p-10">
            <div class="text-center mb-10">
              <div class="inline-flex p-4 rounded-3xl bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 mb-6">
                <UserPlusIcon class="w-10 h-10" />
              </div>
              <h3 class="text-2xl font-black mb-2 text-slate-900 dark:text-white">Neues Konto</h3>
              <p class="text-slate-500">Geben Sie den Namen für das neue Taschengeld-Konto ein.</p>
            </div>
            
            <div class="space-y-6">
              <div>
                <label for="person-name" class="block text-xs font-black uppercase text-slate-400 mb-2 ml-1">Name der Person</label>
                <input id="person-name" ref="nameInput" type="text" v-model="newPersonName" @keyup.enter="addPerson" 
                       placeholder="Spitzname" 
                       class="w-full bg-slate-50 dark:bg-slate-900/50 border-2 border-slate-200 dark:border-slate-700 focus:border-indigo-500 dark:focus:border-indigo-600 rounded-2xl py-4 px-6 focus:outline-none transition-all text-lg font-bold text-slate-900 dark:text-white">
              </div>
              
              <div class="flex flex-col gap-3">
                <button @click="addPerson" :disabled="!newPersonName || txLoading" 
                        class="w-full bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-black py-5 rounded-2xl shadow-xl shadow-indigo-600/20 active:scale-95 transition-all cursor-pointer">
                  <span v-if="txLoading">Wird erstellt...</span>
                  <span v-else>Konto jetzt erstellen</span>
                </button>
                <button @click="showAddPersonModal = false" class="w-full text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 font-bold py-2 transition-colors cursor-pointer capitalize">
                  Abbrechen
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Modal: Add Transaction -->
    <Transition name="modal">
      <div v-if="showTxModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm" @click="closeTxModal"></div>
        <div class="relative bg-white dark:bg-slate-800 rounded-[2.5rem] shadow-2xl w-full max-w-md overflow-hidden border border-slate-200 dark:border-slate-700">
          <div class="h-2 w-full" :class="txForm.type === 'income' ? 'bg-emerald-500' : 'bg-rose-500'"></div>
          
          <div class="p-10">
            <div class="text-center mb-8">
              <div class="inline-flex p-4 rounded-3xl mb-4" :class="txForm.type === 'income' ? 'bg-emerald-50 dark:bg-emerald-900/30 text-emerald-600' : 'bg-rose-50 dark:bg-rose-900/30 text-rose-600'">
                <PlusIcon v-if="txForm.type === 'income'" class="w-8 h-8" />
                <MinusIcon v-else class="w-8 h-8" />
              </div>
              <h3 class="text-2xl font-black mb-1">Buchung für {{ activePerson?.name }}</h3>
              <p class="text-slate-500 capitalize">{{ txForm.type === 'income' ? 'Einnahme' : 'Ausgabe' }} erfassen</p>
            </div>

            <div class="space-y-6">
              <div>
                <label class="block text-xs font-black uppercase text-slate-400 mb-2 ml-1">Betrag (€)</label>
                <div class="relative">
                  <input ref="txAmountInput" type="number" step="0.01" v-model.number="txForm.amount" 
                         :placeholder="txForm.type === 'income' ? 'Taschengeld' : 'Betrag'" 
                         class="w-full bg-slate-50 dark:bg-slate-900/50 border-2 border-slate-100 dark:border-slate-800 focus:border-indigo-500 dark:focus:border-indigo-600 rounded-2xl py-4 px-6 pl-12 focus:outline-none transition-all text-2xl font-black">
                  <span class="absolute left-5 top-1/2 -translate-y-1/2 text-slate-400 font-black text-xl">€</span>
                </div>
              </div>
              
              <div>
                <label class="block text-xs font-black uppercase text-slate-400 mb-2 ml-1">Verwendungszweck</label>
                <input type="text" v-model="txForm.note" 
                       :placeholder="txForm.type === 'income' ? 'Taschengeld' : 'Verwendungszweck'" 
                       class="w-full bg-slate-50 dark:bg-slate-900/50 border-2 border-slate-100 dark:border-slate-800 focus:border-indigo-500 dark:focus:border-indigo-600 rounded-2xl py-4 px-6 focus:outline-none transition-all font-bold">
              </div>

              <div>
                <label class="block text-xs font-black uppercase text-slate-400 mb-2 ml-1">Datum (optional)</label>
                <input type="date" v-model="txForm.date" 
                       class="w-full bg-slate-50 dark:bg-slate-900/50 border-2 border-slate-100 dark:border-slate-800 focus:border-indigo-500 dark:focus:border-indigo-600 rounded-2xl py-4 px-6 focus:outline-none transition-all font-bold">
                <p class="text-xs text-slate-400 mt-1 ml-1">Leer lassen für heutiges Datum</p>
              </div>

              <div class="pt-4 flex flex-col gap-3">
                <button @click="submitTransaction" :disabled="!txForm.amount || txForm.amount <= 0 || txLoading" 
                        class="w-full py-5 rounded-2xl text-white font-black shadow-xl transition-all active:scale-95 disabled:opacity-50 outline-none"
                        :class="txForm.type === 'income' ? 'bg-emerald-600 hover:bg-emerald-700 shadow-emerald-500/20' : 'bg-rose-600 hover:bg-rose-700 shadow-rose-500/20'">
                  <span v-if="txLoading">Übermittle...</span>
                  <span v-else>Buchung bestätigen</span>
                </button>
                <button @click="closeTxModal" class="w-full text-slate-400 font-bold py-2 hover:text-slate-600 transition outline-none">
                  Abbrechen
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Modal: Delete Person -->
    <Transition name="modal">
      <div v-if="showDeleteModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6">
        <div class="absolute inset-0 bg-slate-900/80 backdrop-blur-md" @click="showDeleteModal = false"></div>
        <div class="relative bg-white dark:bg-slate-800 rounded-[2.5rem] shadow-2xl w-full max-w-md border border-slate-200 dark:border-slate-700 overflow-visible transition-all duration-300">
          <div class="p-8 sm:p-10">
            <div class="text-center mb-8">
              <div class="inline-flex p-4 rounded-3xl bg-rose-50 dark:bg-rose-900/30 text-rose-600 mb-6">
                <TrashIcon class="w-10 h-10" />
              </div>
              <h3 class="text-2xl font-black mb-2 text-slate-900 dark:text-white">Konto löschen</h3>
              <p class="text-slate-500">Möchtest du das Konto von <strong class="text-slate-800 dark:text-slate-200">{{ personToDelete?.name }}</strong> wirklich löschen? Diese Aktion kann nicht rückgängig gemacht werden.</p>
            </div>
            
            <div class="flex flex-col gap-3">
              <button @click="executeDeletePerson" 
                      class="w-full bg-rose-600 hover:bg-rose-700 text-white font-black py-5 rounded-2xl shadow-xl shadow-rose-600/20 active:scale-95 transition-all cursor-pointer">
                Endgültig löschen
              </button>
              <button @click="showDeleteModal = false; personToDelete = null" class="w-full text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 font-bold py-2 transition-colors cursor-pointer capitalize">
                Abbrechen
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Modal: Delete Transaction -->
    <Transition name="modal">
      <div v-if="showDeleteTxModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6">
        <div class="absolute inset-0 bg-slate-900/80 backdrop-blur-md" @click="showDeleteTxModal = false"></div>
        <div class="relative bg-white dark:bg-slate-800 rounded-[2.5rem] shadow-2xl w-full max-w-md border border-slate-200 dark:border-slate-700 overflow-visible transition-all duration-300">
          <div class="p-8 sm:p-10">
            <div class="text-center mb-8">
              <div class="inline-flex p-4 rounded-3xl bg-rose-50 dark:bg-rose-900/30 text-rose-600 mb-6">
                <TrashIcon class="w-10 h-10" />
              </div>
              <h3 class="text-2xl font-black mb-2 text-slate-900 dark:text-white">Buchung löschen</h3>
              <p class="text-slate-500">Möchtest du diese Buchung wirklich löschen? Diese Aktion kann nicht rückgängig gemacht werden.</p>
              <div v-if="txToDelete" class="mt-4 p-3 bg-slate-50 dark:bg-slate-900/50 rounded-xl text-sm border border-slate-100 dark:border-slate-700 italic">
                "{{ txToDelete.note || 'Kein Kommentar' }}" ({{ txToDelete.amount.toFixed(2) }} €)
              </div>
            </div>
            
            <div class="flex flex-col gap-3">
              <button @click="executeDeleteTransaction" 
                      class="w-full bg-rose-600 hover:bg-rose-700 text-white font-black py-5 rounded-2xl shadow-xl shadow-rose-600/20 active:scale-95 transition-all cursor-pointer">
                Endgültig löschen
              </button>
              <button @click="showDeleteTxModal = false; txToDelete = null" class="w-full text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 font-bold py-2 transition-colors cursor-pointer capitalize">
                Abbrechen
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Modal: Edit Transaction -->
    <Transition name="modal">
      <div v-if="showEditTxModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm" @click="closeEditTxModal"></div>
        <div class="relative bg-white dark:bg-slate-800 rounded-[2.5rem] shadow-2xl w-full max-w-md overflow-hidden border border-slate-200 dark:border-slate-700">
          <div class="h-2 w-full bg-indigo-500"></div>
          
          <div class="p-10">
            <div class="text-center mb-8">
              <div class="inline-flex p-4 rounded-3xl mb-4 bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600">
                <PencilIcon class="w-8 h-8" />
              </div>
              <h3 class="text-2xl font-black mb-1">Buchung bearbeiten</h3>
              <p class="text-slate-500">Verwendungszweck und Datum anpassen</p>
            </div>

            <div class="space-y-6">
              <div>
                <label class="block text-xs font-black uppercase text-slate-400 mb-2 ml-1">Betrag (€)</label>
                <div class="relative">
                  <input type="number" step="0.01" v-model.number="editTxForm.amount" 
                         class="w-full bg-slate-50 dark:bg-slate-900/50 border-2 border-slate-100 dark:border-slate-800 focus:border-indigo-500 dark:focus:border-indigo-600 rounded-2xl py-4 px-6 pl-12 focus:outline-none transition-all text-2xl font-black">
                  <span class="absolute left-5 top-1/2 -translate-y-1/2 text-slate-400 font-black text-xl">€</span>
                </div>
              </div>
              
              <div>
                <label class="block text-xs font-black uppercase text-slate-400 mb-2 ml-1">Verwendungszweck</label>
                <input type="text" v-model="editTxForm.note" 
                       placeholder="Verwendungszweck" 
                       class="w-full bg-slate-50 dark:bg-slate-900/50 border-2 border-slate-100 dark:border-slate-800 focus:border-indigo-500 dark:focus:border-indigo-600 rounded-2xl py-4 px-6 focus:outline-none transition-all font-bold">
              </div>

              <div>
                <label class="block text-xs font-black uppercase text-slate-400 mb-2 ml-1">Datum</label>
                <input type="date" v-model="editTxForm.date" 
                       class="w-full bg-slate-50 dark:bg-slate-900/50 border-2 border-slate-100 dark:border-slate-800 focus:border-indigo-500 dark:focus:border-indigo-600 rounded-2xl py-4 px-6 focus:outline-none transition-all font-bold">
              </div>

              <div class="pt-4 flex flex-col gap-3">
                <button @click="submitEditTransaction" :disabled="txLoading" 
                        class="w-full py-5 rounded-2xl text-white font-black shadow-xl shadow-indigo-500/20 bg-indigo-600 hover:bg-indigo-700 transition-all active:scale-95 disabled:opacity-50 outline-none">
                  <span v-if="txLoading">Speichern...</span>
                  <span v-else>Änderungen speichern</span>
                </button>
                <button @click="closeEditTxModal" class="w-full text-slate-400 font-bold py-2 hover:text-slate-600 transition outline-none">
                  Abbrechen
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Modal: Add Recurring Transaction -->
    <Transition name="modal">
      <div v-if="showAddRecurringModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm" @click="closeRecurringModal"></div>
        <div class="relative bg-white dark:bg-slate-800 rounded-[2.5rem] shadow-2xl w-full max-w-md overflow-hidden border border-slate-200 dark:border-slate-700">
          <div class="h-2 w-full bg-indigo-500"></div>
          <div class="p-10">
            <div class="text-center mb-8">
              <div class="inline-flex p-4 rounded-3xl mb-4 bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600">
                <ArrowPathIcon class="w-8 h-8" />
              </div>
              <h3 class="text-2xl font-black mb-1">{{ editingRecurring ? 'Abo bearbeiten' : 'Neues Abo' }}</h3>
              <p class="text-slate-500">Wiederkehrende Buchung einrichten</p>
            </div>

            <div class="space-y-6">
              <div>
                <label class="block text-xs font-black uppercase text-slate-400 mb-2 ml-1">Konto</label>
                <select v-model="recurringForm.person_id" 
                        class="w-full bg-slate-50 dark:bg-slate-900/50 border-2 border-slate-100 dark:border-slate-800 focus:border-indigo-500 dark:focus:border-indigo-600 rounded-2xl py-4 px-6 focus:outline-none transition-all font-bold">
                  <option v-for="p in persons" :key="p.id" :value="p.id">{{ p.name }}</option>
                </select>
              </div>

              <div>
                <label class="block text-xs font-black uppercase text-slate-400 mb-2 ml-1">Betrag (€)</label>
                <div class="relative">
                  <input type="number" step="0.01" v-model.number="recurringForm.amount" 
                         placeholder="-29.99 für Ausgabe" 
                         class="w-full bg-slate-50 dark:bg-slate-900/50 border-2 border-slate-100 dark:border-slate-800 focus:border-indigo-500 dark:focus:border-indigo-600 rounded-2xl py-4 px-6 pl-12 focus:outline-none transition-all text-2xl font-black">
                  <span class="absolute left-5 top-1/2 -translate-y-1/2 text-slate-400 font-black text-xl">€</span>
                </div>
              </div>

              <div>
                <label class="block text-xs font-black uppercase text-slate-400 mb-2 ml-1">Beschreibung</label>
                <input type="text" v-model="recurringForm.note" 
                       placeholder="z.B. Fitnessstudio" 
                       class="w-full bg-slate-50 dark:bg-slate-900/50 border-2 border-slate-100 dark:border-slate-800 focus:border-indigo-500 dark:focus:border-indigo-600 rounded-2xl py-4 px-6 focus:outline-none transition-all font-bold">
              </div>

              <div>
                <label class="block text-xs font-black uppercase text-slate-400 mb-2 ml-1">Intervall</label>
                <div class="grid grid-cols-2 gap-2">
                  <button v-for="intv in intervals" :key="intv.value" 
                          @click="recurringForm.interval = intv.value"
                          class="py-3 px-4 rounded-xl font-bold text-sm transition-all border-2"
                          :class="recurringForm.interval === intv.value ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600' : 'border-slate-200 dark:border-slate-700 hover:border-slate-300'">
                    {{ intv.label }}
                  </button>
                </div>
              </div>

              <div>
                <label class="block text-xs font-black uppercase text-slate-400 mb-2 ml-1">Startdatum</label>
                <input type="date" v-model="recurringForm.start_date" 
                       class="w-full bg-slate-50 dark:bg-slate-900/50 border-2 border-slate-100 dark:border-slate-800 focus:border-indigo-500 dark:focus:border-indigo-600 rounded-2xl py-4 px-6 focus:outline-none transition-all font-bold">
              </div>

              <div class="pt-4 flex flex-col gap-3">
                <button @click="submitRecurring" :disabled="!recurringForm.amount || !recurringForm.person_id || txLoading" 
                        class="w-full py-5 rounded-2xl text-white font-black shadow-xl shadow-indigo-500/20 bg-indigo-600 hover:bg-indigo-700 transition-all active:scale-95 disabled:opacity-50 outline-none">
                  <span v-if="txLoading">Speichern...</span>
                  <span v-else>{{ editingRecurring ? 'Änderungen speichern' : 'Abo erstellen' }}</span>
                </button>
                <button @click="closeRecurringModal" class="w-full text-slate-400 font-bold py-2 hover:text-slate-600 transition outline-none">
                  Abbrechen
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Modal: Delete Recurring -->
    <Transition name="modal">
      <div v-if="showDeleteRecurringModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm" @click="showDeleteRecurringModal = false"></div>
        <div class="relative bg-white dark:bg-slate-800 rounded-[2.5rem] shadow-2xl w-full max-w-md overflow-hidden border border-slate-200 dark:border-slate-700">
          <div class="p-10">
            <div class="text-center mb-8">
              <div class="inline-flex p-4 rounded-3xl mb-4 bg-rose-50 dark:bg-rose-900/30 text-rose-600">
                <TrashIcon class="w-8 h-8" />
              </div>
              <h3 class="text-2xl font-black mb-1">Abo löschen</h3>
              <p class="text-slate-500">Möchtest du dieses Abo wirklich löschen?</p>
              <div v-if="recurringToDelete" class="mt-4 p-3 bg-slate-50 dark:bg-slate-900/50 rounded-xl text-sm border border-slate-100 dark:border-slate-700">
                "{{ recurringToDelete.note }}" ({{ recurringToDelete.amount.toFixed(2) }} € / {{ getIntervalLabel(recurringToDelete.interval) }})
              </div>
            </div>
            <div class="flex flex-col gap-3">
              <button @click="executeDeleteRecurring" class="w-full py-5 rounded-2xl text-white font-black bg-rose-600 hover:bg-rose-700 shadow-xl shadow-rose-600/20 transition-all active:scale-95">
                Endgültig löschen
              </button>
              <button @click="showDeleteRecurringModal = false; recurringToDelete = null" class="w-full text-slate-400 font-bold py-2 hover:text-slate-600 transition">
                Abbrechen
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, nextTick } from 'vue'
import axios from 'axios'
import { format, parseISO, startOfMonth } from 'date-fns'
import { de } from 'date-fns/locale'

// Heroicons
import { 
  BanknotesIcon, PlusIcon, MinusIcon, WalletIcon, 
  ArrowTrendingUpIcon, ArrowTrendingDownIcon, UserGroupIcon,
  ChartBarIcon, TrashIcon, ListBulletIcon, XMarkIcon,
  CheckCircleIcon, XCircleIcon, ClockIcon, UserPlusIcon,
  SunIcon, MoonIcon, UserIcon, ArrowDownTrayIcon, ArrowUpTrayIcon,
  MagnifyingGlassIcon, PencilIcon, ArrowPathIcon, CalendarIcon,
  ChevronLeftIcon, ChevronRightIcon
} from '@heroicons/vue/24/solid'

// Chart.js imports
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(
  CategoryScale, LinearScale, PointElement, LineElement, 
  Title, Tooltip, Legend, Filler
)

// Ingress awareness routing
const baseApiUrl = (window.dynamicBase || '/') + 'api/'

// State
const isDark = ref(localStorage.getItem('theme') === 'dark')
const loading = ref(true)
const txLoading = ref(false)
const error = ref('')
const success = ref('')
const persons = ref([])
const recentTransactions = ref([])
const activeChartView = ref(null)
const chartData = ref(null)
const selectedAccountId = ref(null)
const searchQuery = ref('')
const filterDateFrom = ref('')
const filterDateTo = ref('')
const allTransactions = ref([]) // For history searching
const activeTab = ref('dashboard')
const recurringTransactions = ref([])
const currentYear = ref(new Date().getFullYear())
const monthNames = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
const intervals = [
  { value: 'daily', label: 'Täglich' },
  { value: 'weekly', label: 'Wöchentlich' },
  { value: 'monthly', label: 'Monatlich' },
  { value: 'quarterly', label: 'Quartalsweise' }
]

// Computed Stats
const totalBalance = computed(() => persons.value.reduce((acc, p) => acc + (p.balance || 0), 0))

const monthlyIncome = computed(() => {
  const start = startOfMonth(new Date())
  return recentTransactions.value
    .filter(t => new Date(t.date) >= start && t.amount > 0)
    .reduce((acc, t) => acc + t.amount, 0)
})

const monthlyExpenses = computed(() => {
  const start = startOfMonth(new Date())
  return Math.abs(recentTransactions.value
    .filter(t => new Date(t.date) >= start && t.amount < 0)
    .reduce((acc, t) => acc + t.amount, 0))
})

const filteredTransactions = computed(() => {
  if (!selectedAccountId.value) return recentTransactions.value
  return recentTransactions.value.filter(t => t.person_id === selectedAccountId.value)
})

const historyTransactions = computed(() => {
  let list = allTransactions.value
  
  // Filter by selected account
  if (selectedAccountId.value) {
    list = list.filter(t => t.person_id === selectedAccountId.value)
  }
  
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(t => {
      const noteMatch = t.note?.toLowerCase().includes(q)
      const personMatch = getPersonName(t.person_id).toLowerCase().includes(q)
      return noteMatch || personMatch
    })
  }
  
  if (filterDateFrom.value) {
    const from = new Date(filterDateFrom.value)
    list = list.filter(t => new Date(t.date) >= from)
  }
  
  if (filterDateTo.value) {
    const to = new Date(filterDateTo.value)
    // End of day for to-date
    to.setHours(23, 59, 59, 999)
    list = list.filter(t => new Date(t.date) <= to)
  }
  
  return list
})

// Chart Configuration
const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: isDark.value ? '#1e293b' : '#fff',
      titleColor: isDark.value ? '#f1f5f9' : '#0f172a',
      bodyColor: isDark.value ? '#94a3b8' : '#64748b',
      borderColor: isDark.value ? '#334155' : '#e2e8f0',
      borderWidth: 1,
      padding: 12,
      displayColors: false,
      callbacks: {
        label: context => ` ${context.parsed.y.toFixed(2)} €`
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: { color: isDark.value ? 'rgba(51, 65, 85, 0.4)' : 'rgba(226, 232, 240, 0.6)', drawBorder: false },
      ticks: { color: isDark.value ? '#64748b' : '#94a3b8', callback: value => `${value} €` }
    },
    x: {
      grid: { display: false },
      ticks: { color: isDark.value ? '#64748b' : '#94a3b8' }
    }
  },
  interaction: { mode: 'index', intersect: false },
  elements: { line: { tension: 0.4 }, point: { hitRadius: 20 } }
}))

// Modals
const showAddPersonModal = ref(false)
const newPersonName = ref('')
const nameInput = ref(null)
const showTxModal = ref(false)
const activePerson = ref(null)
const txForm = ref({ type: 'expense', amount: null, note: '', date: '' })
const txAmountInput = ref(null)
const showDeleteModal = ref(false)
const personToDelete = ref(null)
const showDeleteTxModal = ref(false)
const txToDelete = ref(null)
const showEditTxModal = ref(false)
const editTxForm = ref({ id: null, amount: null, note: '', date: '' })
const showAddRecurringModal = ref(false)
const showDeleteRecurringModal = ref(false)
const recurringToDelete = ref(null)
const editingRecurring = ref(false)
const recurringForm = ref({ id: null, person_id: null, amount: null, note: '', interval: 'monthly', start_date: '' })

// Focus logic
watch(showAddPersonModal, async (val) => {
  if (val) {
    await nextTick()
    nameInput.value?.focus()
  }
})

watch(showTxModal, async (val) => {
  if (val) {
    await nextTick()
    txAmountInput.value?.focus()
  }
})

// Lifecycle
onMounted(() => {
  // Initialize theme
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
  fetchData()
})

const toggleDarkMode = () => {
  isDark.value = !isDark.value
  console.log('Toggling theme. isDark:', isDark.value)
  const root = document.documentElement
  root.classList.toggle('dark', isDark.value)
  console.log('HTML ClassList:', root.className)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

const fetchData = async (silent = false) => {
  loading.value = true
  try {
    const [pRes, tRes, allRes] = await Promise.all([
      axios.get(`${baseApiUrl}accounts/`),
      axios.get(`${baseApiUrl}transactions/?limit=50`),
      axios.get(`${baseApiUrl}transactions/?limit=10000`)
    ])
    persons.value = pRes.data
    recentTransactions.value = tRes.data
    allTransactions.value = allRes.data
    
    // Load recurring transactions separately (may fail if table doesn't exist yet)
    try {
      const rRes = await axios.get(`${baseApiUrl}recurring/`)
      recurringTransactions.value = rRes.data
    } catch (e) {
      console.warn('Recurring transactions not available:', e)
      recurringTransactions.value = []
    }
    
    // Execute due recurring transactions (fire and forget)
    axios.post(`${baseApiUrl}recurring/execute`).catch(e => {
      console.warn('Recurring execution check failed:', e)
    })
  } catch (err) {
    if (!silent) showError('Verbindung zum Server fehlgeschlagen.')
    if (!silent) throw err
  } finally {
    loading.value = false
  }
}

const getPersonStats = (id) => {
  const start = startOfMonth(new Date())
  const txs = allTransactions.value.filter(t => t.person_id === id && new Date(t.date) >= start)
  return {
    income: txs.filter(t => t.amount > 0).reduce((acc, t) => acc + t.amount, 0),
    expense: Math.abs(txs.filter(t => t.amount < 0).reduce((acc, t) => acc + t.amount, 0))
  }
}

const exportData = () => {
  window.open(`${baseApiUrl}export`, '_blank')
}

const importData = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  const formData = new FormData()
  formData.append('file', file)
  
  try {
    loading.value = true
    const res = await axios.post(`${baseApiUrl}import`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    await fetchData()
    showSuccess(res.data.message)
  } catch (err) {
    showError('Import fehlgeschlagen: ' + (err.response?.data?.detail || 'Unbekannter Fehler'))
  } finally {
    loading.value = false
  }
}

const addPerson = async () => {
  if (!newPersonName.value || txLoading.value) return
  txLoading.value = true
  const personName = newPersonName.value
  try {
    // Ensure we send correct payload as expected by backend (AccountCreate)
    await axios.post(`${baseApiUrl}accounts/`, { name: personName })
    await fetchData()
    showAddPersonModal.value = false
    newPersonName.value = ''
    showSuccess(`${personName} wurde erfolgreich angelegt.`)
  } catch (err) {
    showError(err.response?.data?.detail || 'Fehler beim Anlegen. Name evtl. schon vergeben?')
  } finally {
    txLoading.value = false
  }
}

const confirmDeletePerson = (person) => {
  personToDelete.value = person
  showDeleteModal.value = true
}

const executeDeletePerson = async () => {
  if (!personToDelete.value) return
  const { id, name } = personToDelete.value
  
  try {
    await axios.delete(`${baseApiUrl}accounts/${id}`)
    // UI REAKTIVITÄT: Sofort lokal filtern
    persons.value = persons.value.filter(p => p.id !== id)
    recentTransactions.value = recentTransactions.value.filter(t => t.person_id !== id)
    
    showDeleteModal.value = false
    personToDelete.value = null
    
    // Reset filter if the deleted account was selected
    if (selectedAccountId.value === id) selectedAccountId.value = null
    
    // Dann zur Sicherheit neu laden
    await fetchData()
    if (activeChartView.value?.id === id) activeChartView.value = null
    showSuccess(`Konto von ${name} wurde entfernt.`)
  } catch (err) {
     showError('Fehler beim Löschen des Kontos.')
  }
}

const openTxModal = (person, type = 'expense') => {
  activePerson.value = person
  txForm.value = { type, amount: null, note: '', date: '' }
  showTxModal.value = true
}

const closeTxModal = () => {
  showTxModal.value = false
  activePerson.value = null
}

const toggleAccountFilter = (id) => {
  if (selectedAccountId.value === id) {
    selectedAccountId.value = null
  } else {
    selectedAccountId.value = id
  }
}

const submitTransaction = async () => {
  if (!txForm.value.amount || txForm.value.amount <= 0 || !activePerson.value || txLoading.value) return
  txLoading.value = true
  
  const finalAmount = txForm.value.type === 'expense' ? -Math.abs(txForm.value.amount) : Math.abs(txForm.value.amount)
  
  const payload = {
    person_id: activePerson.value.id,
    amount: finalAmount,
    note: txForm.value.note
  }
  
  if (txForm.value.date) {
    payload.date = new Date(txForm.value.date).toISOString()
  }
  
  try {
    await axios.post(`${baseApiUrl}transactions/`, payload)
    closeTxModal()
    showSuccess('Buchung erfolgreich gespeichert.')
    
    // Daten neu laden, aber Fehler hier nicht als Speicherfehler anzeigen
    try {
      await fetchData(true) // silent=true, um Fehler-Popup zu vermeiden
      if (activeChartView.value?.id === activePerson.value.id) viewDetails(activePerson.value)
    } catch (fetchErr) {
      console.warn('Daten konnten nicht neu geladen werden:', fetchErr)
    }
  } catch (err) {
    showError('Fehler beim Speichern der Buchung.')
  } finally {
    txLoading.value = false
  }
}

const confirmDeleteTransaction = (tx) => {
  txToDelete.value = tx
  showDeleteTxModal.value = true
}

const executeDeleteTransaction = async () => {
  if (!txToDelete.value) return
  const id = txToDelete.value.id
  
  try {
    await axios.delete(`${baseApiUrl}transactions/${id}`)
    
    // UI REAKTIVITÄT: Sofort lokal filtern
    recentTransactions.value = recentTransactions.value.filter(t => t.id !== id)
    
    showDeleteTxModal.value = false
    txToDelete.value = null
    
    await fetchData()
    if (activeChartView.value) viewDetails(activeChartView.value)
    showSuccess('Buchung entfernt.')
  } catch (err) {
    showError('Fehler beim Löschen.')
  }
}

const openEditTxModal = (tx) => {
  editTxForm.value = {
    id: tx.id,
    amount: tx.amount,
    note: tx.note || '',
    date: tx.date ? tx.date.split('T')[0] : ''
  }
  showEditTxModal.value = true
}

const closeEditTxModal = () => {
  showEditTxModal.value = false
  editTxForm.value = { id: null, amount: null, note: '', date: '' }
}

const submitEditTransaction = async () => {
  if (!editTxForm.value.id || txLoading.value) return
  txLoading.value = true
  
  try {
    const updateData = {}
    if (editTxForm.value.note !== undefined) updateData.note = editTxForm.value.note
    if (editTxForm.value.date) updateData.date = new Date(editTxForm.value.date).toISOString()
    if (editTxForm.value.amount !== undefined) updateData.amount = editTxForm.value.amount
    
    await axios.put(`${baseApiUrl}transactions/${editTxForm.value.id}`, updateData)
    closeEditTxModal()
    showSuccess('Buchung erfolgreich aktualisiert.')
    
    try {
      await fetchData(true)
      if (activeChartView.value) viewDetails(activeChartView.value)
    } catch (fetchErr) {
      console.warn('Daten konnten nicht neu geladen werden:', fetchErr)
    }
  } catch (err) {
    showError('Fehler beim Aktualisieren der Buchung.')
  } finally {
    txLoading.value = false
  }
}

const viewDetails = async (person) => {
  activeChartView.value = person
  try {
    const res = await axios.get(`${baseApiUrl}accounts/${person.id}`)
    const txs = res.data.transactions.slice().sort((a,b) => new Date(a.date) - new Date(b.date))
    
    if (txs.length === 0) {
      chartData.value = null
      return
    }

    const labels = []
    const dataPoints = []
    let runningBalance = 0
    txs.forEach(t => {
      runningBalance += t.amount
      labels.push(format(parseISO(t.date), 'dd.MM', { locale: de }))
      dataPoints.push(runningBalance)
    })

    const isPos = runningBalance >= 0
    chartData.value = {
      labels,
      datasets: [{
        label: 'Saldo',
        data: dataPoints,
        borderColor: isPos ? '#10b981' : '#f43f5e',
        backgroundColor: isPos ? 'rgba(16, 185, 129, 0.1)' : 'rgba(244, 63, 94, 0.1)',
        fill: true,
        borderWidth: 4,
        pointBackgroundColor: '#fff',
        pointBorderWidth: 3,
        pointRadius: 4,
        pointHoverRadius: 8
      }]
    }
    setTimeout(() => { window.scrollTo({ top: 400, behavior: 'smooth' }) }, 100)
  } catch (err) {
    showError('Fehler beim Laden der Historiendaten.')
  }
}

// Helpers
const showSuccess = (msg) => {
  success.value = msg
  setTimeout(() => { success.value = '' }, 5000)
}

const showError = (msg) => {
  error.value = msg
  setTimeout(() => { error.value = '' }, 5000)
}

const getPersonName = id => persons.value.find(p => p.id === id)?.name || 'Unbekannt'
const formatDate = str => str ? format(new Date(str), 'dd.MM.yyyy', { locale: de }) : ''

const getIntervalLabel = (interval) => {
  const labels = { daily: 'Täglich', weekly: 'Wöchentlich', monthly: 'Monatlich', quarterly: 'Quartalsweise' }
  return labels[interval] || interval
}

// Recurring Transaction Functions
const closeRecurringModal = () => {
  showAddRecurringModal.value = false
  editingRecurring.value = false
  recurringForm.value = { id: null, person_id: persons.value[0]?.id || null, amount: null, note: '', interval: 'monthly', start_date: '' }
}

const openEditRecurringModal = (rt) => {
  editingRecurring.value = true
  recurringForm.value = {
    id: rt.id,
    person_id: rt.person_id,
    amount: rt.amount,
    note: rt.note || '',
    interval: rt.interval,
    start_date: rt.start_date ? rt.start_date.split('T')[0] : ''
  }
  showAddRecurringModal.value = true
}

const submitRecurring = async () => {
  if (!recurringForm.value.amount || !recurringForm.value.person_id || txLoading.value) return
  txLoading.value = true
  
  const payload = {
    person_id: recurringForm.value.person_id,
    amount: recurringForm.value.amount,
    note: recurringForm.value.note,
    interval: recurringForm.value.interval,
    start_date: recurringForm.value.start_date ? new Date(recurringForm.value.start_date).toISOString() : new Date().toISOString(),
    active: true
  }
  
  try {
    if (editingRecurring.value && recurringForm.value.id) {
      await axios.put(`${baseApiUrl}recurring/${recurringForm.value.id}`, payload)
      showSuccess('Abo erfolgreich aktualisiert.')
    } else {
      await axios.post(`${baseApiUrl}recurring/`, payload)
      showSuccess('Abo erfolgreich erstellt.')
    }
    closeRecurringModal()
    await fetchData(true)
  } catch (err) {
    showError('Fehler beim Speichern des Abos.')
  } finally {
    txLoading.value = false
  }
}

const confirmDeleteRecurring = (rt) => {
  recurringToDelete.value = rt
  showDeleteRecurringModal.value = true
}

const executeDeleteRecurring = async () => {
  if (!recurringToDelete.value) return
  const id = recurringToDelete.value.id
  
  try {
    await axios.delete(`${baseApiUrl}recurring/${id}`)
    recurringTransactions.value = recurringTransactions.value.filter(r => r.id !== id)
    showDeleteRecurringModal.value = false
    recurringToDelete.value = null
    showSuccess('Abo gelöscht.')
  } catch (err) {
    showError('Fehler beim Löschen des Abos.')
  }
}

// Yearly Overview Functions
const getYearlyProjection = (personId, monthIndex) => {
  const now = new Date()
  const targetMonth = new Date(currentYear.value, monthIndex, 1)
  
  // Get actual transactions for this month
  const monthTxs = allTransactions.value.filter(t => {
    const txDate = new Date(t.date)
    return t.person_id === personId && 
           txDate.getFullYear() === currentYear.value && 
           txDate.getMonth() === monthIndex
  })
  
  const actualIncome = monthTxs.filter(t => t.amount > 0).reduce((acc, t) => acc + t.amount, 0)
  const actualExpense = Math.abs(monthTxs.filter(t => t.amount < 0).reduce((acc, t) => acc + t.amount, 0))
  
  // Get recurring transactions for projection
  const personRecurring = recurringTransactions.value.filter(r => r.person_id === personId && r.active)
  let projectedIncome = 0
  let projectedExpense = 0
  
  personRecurring.forEach(r => {
    if (r.amount > 0) {
      if (r.interval === 'monthly') projectedIncome += r.amount
      else if (r.interval === 'quarterly' && monthIndex % 3 === 0) projectedIncome += r.amount
      else if (r.interval === 'weekly') projectedIncome += r.amount * 4
      else if (r.interval === 'daily') projectedIncome += r.amount * 30
    } else {
      if (r.interval === 'monthly') projectedExpense += Math.abs(r.amount)
      else if (r.interval === 'quarterly' && monthIndex % 3 === 0) projectedExpense += Math.abs(r.amount)
      else if (r.interval === 'weekly') projectedExpense += Math.abs(r.amount) * 4
      else if (r.interval === 'daily') projectedExpense += Math.abs(r.amount) * 30
    }
  })
  
  // Calculate running balance
  let balance = 0
  // Get balance up to start of year
  const yearStart = new Date(currentYear.value, 0, 1)
  const priorTxs = allTransactions.value.filter(t => t.person_id === personId && new Date(t.date) < yearStart)
  balance = priorTxs.reduce((acc, t) => acc + t.amount, 0)
  
  // Add up months until target
  for (let m = 0; m <= monthIndex; m++) {
    const mTxs = allTransactions.value.filter(t => {
      const txDate = new Date(t.date)
      return t.person_id === personId && 
             txDate.getFullYear() === currentYear.value && 
             txDate.getMonth() === m
    })
    balance += mTxs.reduce((acc, t) => acc + t.amount, 0)
    
    // Add projected recurring for future months or current month if past
    if (targetMonth > now || m === now.getMonth()) {
      // Already included in actual transactions
    }
  }
  
  // For future months, add projected recurring
  if (targetMonth > now) {
    const monthsAhead = monthIndex - now.getMonth()
    personRecurring.forEach(r => {
      let multiplier = 0
      if (r.interval === 'monthly') multiplier = monthsAhead
      else if (r.interval === 'quarterly') multiplier = Math.floor(monthsAhead / 3)
      else if (r.interval === 'weekly') multiplier = monthsAhead * 4
      else if (r.interval === 'daily') multiplier = monthsAhead * 30
      balance += r.amount * multiplier
    })
  }
  
  return {
    balance,
    income: actualIncome || projectedIncome,
    expense: actualExpense || projectedExpense
  }
}
</script>

<style scoped>

.modal-enter-active, .modal-leave-active { transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
.modal-enter-from, .modal-leave-to { opacity: 0; transform: scale(0.95) translateY(20px); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.5s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.toast-enter-active, .toast-leave-active { transition: all 0.4s ease; }
.toast-enter-from { opacity: 0; transform: translateX(100px); }
.toast-leave-to { opacity: 0; transform: scale(0.9); }
</style>
