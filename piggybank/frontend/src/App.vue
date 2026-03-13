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
        <!-- Deleted Global Stats Section as per point 4 -->

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
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 dark:divide-slate-700/30">
                <tr v-for="tx in historyTransactions" :key="tx.id" class="hover:bg-slate-50 dark:hover:bg-slate-700/20 transition-colors">
                  <td class="px-8 py-4 whitespace-nowrap text-sm text-slate-500 font-medium">{{ formatDate(tx.date) }}</td>
                  <td class="px-8 py-4">
                    <span class="inline-flex items-center gap-2 font-bold text-sm">
                       {{ getPersonName(tx.person_id) }}
                    </span>
                  </td>
                  <td class="px-8 py-4 text-sm text-slate-600 dark:text-slate-400">"{{ tx.note || '-' }}"</td>
                  <td class="px-8 py-4 whitespace-nowrap text-right font-black" :class="tx.amount > 0 ? 'text-emerald-500' : 'text-rose-500'">
                    {{ tx.amount > 0 ? '+' : '' }}{{ tx.amount.toFixed(2) }} €
                  </td>
                </tr>
                <tr v-if="historyTransactions.length === 0">
                  <td colspan="4" class="px-8 py-10 text-center text-slate-400 italic text-sm">Keine Einträge für diese Suche gefunden.</td>
                </tr>
              </tbody>
            </table>
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
                       placeholder="z.B. Sandra" 
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
                  <input type="number" step="0.01" v-model.number="txForm.amount" 
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
  MagnifyingGlassIcon
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
const txForm = ref({ type: 'expense', amount: null, note: '' })
const showDeleteModal = ref(false)
const personToDelete = ref(null)
const showDeleteTxModal = ref(false)
const txToDelete = ref(null)

// Focus logic
watch(showAddPersonModal, async (val) => {
  if (val) {
    await nextTick()
    nameInput.value?.focus()
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

const fetchData = async () => {
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
  } catch (err) {
    showError('Verbindung zum Server fehlgeschlagen.')
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
    showSuccess(res.data.message)
    await fetchData()
  } catch (err) {
    showError('Import fehlgeschlagen: ' + (err.response?.data?.detail || 'Unbekannter Fehler'))
  } finally {
    loading.value = false
  }
}

const addPerson = async () => {
  if (!newPersonName.value || txLoading.value) return
  txLoading.value = true
  try {
    // Ensure we send correct payload as expected by backend (AccountCreate)
    await axios.post(`${baseApiUrl}accounts/`, { name: newPersonName.value })
    await fetchData()
    showSuccess(`${newPersonName.value} wurde erfolgreich angelegt.`)
    showAddPersonModal.value = false
    newPersonName.value = ''
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
    showSuccess(`Konto von ${name} wurde entfernt.`)
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
  } catch (err) {
     showError('Fehler beim Löschen des Kontos.')
  }
}

const openTxModal = (person, type = 'expense') => {
  activePerson.value = person
  txForm.value = { type, amount: null, note: '' }
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
  
  try {
    await axios.post(`${baseApiUrl}transactions/`, {
      person_id: activePerson.value.id,
      amount: finalAmount,
      note: txForm.value.note
    })
    closeTxModal()
    showSuccess('Buchung erfolgreich gespeichert.')
    await fetchData()
    if (activeChartView.value?.id === activePerson.value.id) viewDetails(activePerson.value)
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
    showSuccess('Buchung entfernt.')
    
    // UI REAKTIVITÄT: Sofort lokal filtern
    recentTransactions.value = recentTransactions.value.filter(t => t.id !== id)
    
    showDeleteTxModal.value = false
    txToDelete.value = null
    
    await fetchData()
    if (activeChartView.value) viewDetails(activeChartView.value)
  } catch (err) {
    showError('Fehler beim Löschen.')
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
