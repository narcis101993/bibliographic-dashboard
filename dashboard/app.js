(function () {
  "use strict";

  var LANG_KEY = "stamatie-dashboard-lang";
  var DARK_KEY = "stamatie-dashboard-dark";
  var PAGE_SIZE = 10;
  var PUB_PAGE_SIZE = 5;
  var CIT_PAGE_SIZE = 5;
  var PALETTE = ["#12324d", "#2a7396", "#4c9fbf", "#8fc3d8", "#b9c6d4", "#e2b84b", "#2f8a5b", "#5b45a3", "#b3403a"];

  var I18N = {
    ro: {
      appTitle: "Dashboard bibliografic",
      appSubtitle: "Gabriela Daniela Stamatie (Criveanu-Stamatie) · IBA București",
      updated: "Actualizat",
      redetect: "Re-detectează",
      rescanning: "Se scanează…",
      refreshData: "Reîncarcă",
      detected: "Versiune detectată automat: {v}",
      notDetected: "Versiune nedetectată",
      rule: "regulă: versiune numerică maximă comună",
      modeEmbedded: "date încorporate (file://)",
      modeCsv: "CSV încărcate la runtime",
      modeManifest: "manifest detectat",
      noCommon: "nicio versiune comună găsită",
      tabPublications: "Publicații",
      tabCitations: "Citări",
      tabSynthesis: "Sinteză",
      exportCsv: "Export CSV",
      exportXlsx: "Descarcă XLSX",
      search: "Caută",
      pubSearchPh: "Titlu, autor, DOI…",
      citSearchPh: "Lucrare citată, autor, DOI…",
      author: "Autor / co-autor",
      authorPh: "Nume autor…",
      year: "An",
      citYear: "An citare",
      allYears: "Toți anii",
      type: "Tip",
      allTypes: "Toate tipurile",
      venue: "Revistă",
      allVenues: "Toate revistele",
      article: "Articol citat",
      allArticles: "Toate articolele",
      doiOnly: "Doar cu DOI",
      excludeSelf: "Exclude auto-citări",
      reset: "Resetează",
      chartsToggle: "Grafice",
      pageSize: "Pe pagină",
      removeFilter: "Elimină filtrul",
      toastFresh: "Datele afișate sunt la zi",
      toastUpdated: "Date actualizate",
      footDashboard: "Dashboard bibliografic",
      footCreated: "Creat de",
      footWith: "cu ajutorul",
      multiSelected: "{n} selectate",
      pubFilterNote: "Filtrele se aplică instantaneu pe datele versiunii detectate.",
      citFilterNote: "Auto-citările sunt evidențiate; totalurile reflectă filtrele active.",
      pubTableTitle: "Centralizator",
      citTableTitle: "Lucrări citante",
      colNr: "Nr.",
      colYear: "An",
      colTitle: "Titlu",
      colVenue: "Revistă",
      colType: "Tip",
      colDoi: "DOI",
      colLink: "Link",
      colAuthors: "Autori",
      colVolume: "Volum/Issue",
      colCitations: "Citări",
      colSelf: "Auto-citare",
      colNotes: "Observații",
      dateCitations: "Citări",
      pillStale: "necesită actualizare",
      synTitleFilter: "Titlu articol",
      scholarExportTitle: "Google Scholar (export)",
      scholarExportCap: "Lucrări de pe Scholar care nu sunt încă în centralizator.",
      synTitleFilterPh: "Filtrează după titlu articol…",
      colArticle: "Art.",
      colCitYear: "An citare",
      colCiting: "Lucrare citantă",
      firstPage: "Prima pagină",
      lastPage: "Ultima pagină",
      prevPage: "Pagina anterioară",
      nextPage: "Pagina următoare",
      pageLabel: "Pagina",
      prev: "Anterior",
      next: "Următor",
      pageOf: "Pagina {page} / {pages}",
      showingRange: "Afișate {from}–{to} din {total}",
      noResults: "Nicio înregistrare pentru filtrele selectate.",
      noResultsNote: "Filtrele active au eliminat toate rezultatele. Redu filtrele sau resetează-le.",
      resultsFound: "{total} din {all}",
      copyLink: "Copiază link",
      linkCopied: "Link copiat",
      linkCopyFail: "Copierea a eșuat",
      noDoi: "fără DOI",
      untitled: "Fără titlu",
      yes: "Da",
      no: "Nu",
      pubPanelSub: "{n} înregistrări · {articles} articole · {doi} cu DOI",
      citPanelSub: "{n} lucrări citante · {links} legături · {self} auto-citări",
      kpiCiting: "Lucrări citante",
      kpiLinks: "Legături citare",
      kpiSelf: "Auto-citări",
      kpiSelfLinks: "Legături auto-citare",
      kpiExternalLinks: "Legături externe citare",
      kpiMaxYear: "An maxim",
      kpiHighlighted: "evidențiate",
      kpiPublications: "Publicații",
      kpiNoCitations: "Articole fără citări",
      kpiExternalSub: "{n} lucrări externe",
      kpiLinksSub: "{n} legături externe",
      kpiMaxYearSub: "{n} legături",
      synPubsSub: "{articles} articole + {other}",
      synWorksSub: "{n} lucrări externe",
      synLinksSub: "{n} legături externe",
      synMissingSub: "din {n}",
      pubByYear: "Publicații pe an",
      pubByYearCap: "Înregistrări pe an de publicare (filtrate).",
      pubTypes: "Tipuri de publicații",
      pubTypesCap: "Distribuție pe tipuri (filtrate).",
      citByYear: "Citări pe an",
      citByYearCap: "Legături de citare pe an de citare (filtrate).",
      topCited: "Top articole citate",
      topCitedCap: "Legături de citare per articol (filtrate).",
      citTypes: "Tipuri de lucrări citante",
      synPanelSub: "Indicatori, matrice articol × an de citare și acoperirea datelor.",
      synMatrix: "Matrice articol × an de citare",
      pillAllData: "toate datele",
      synMatrixCap: "Celulele numără legăturile de citare; rândurile pot totaliza mai mult decât lucrările unice.",
      matrixArticle: "Art.",
      matrixTotal: "Total",
      coverage: "Acoperire date",
      coverageBadge: "{n} fără citări",
      coverageCap: "Articolele fără legături de citare sunt marcate separat.",
      coveragePartialBadge: "{n} parțial verificate",
      coveragePartialCap: "Articole fără identificator, în curs de re-verificare.",
      coveragePartialNote: "Nu sunt incluse în cifrele de „fără citări” conform metodologiei.",
      qa: "QA & recomandări",
      qa1: "{links} legături → {works} lucrări unice; {self} auto-citări ({external} externe).",
      qa2: "Eșantion de 10 DOI-uri de citare verificate Crossref: 10/10.",
      qa3: "Numărătoarea este un minim (OpenAlex); Scopus/WoS/Google Scholar lipsesc.",
      qa4: "De re-verificat: #5, #6, #8, #14, #19 și articolele din 2026.",
      pubDetails: "Detalii articol",
      pubDetailsAuthors: "Toți autorii",
      pubDetailsVolume: "Volum/Issue",
      pubDetailsPages: "Pagini",
      pubDetailsIssn: "ISSN",
      pubDetailsPmid: "PMID/PMCID",
      pubDetailsSource: "Sursa",
      pubDetailsNotes: "Note",
      pubDetailsCoverage: "Acoperire",
      pubDetailsConfidence: "Încredere",
      pubDetailsCoverageNote: "Notă acoperire",
      pubDetailsLink: "Link",
      pubDetailsPosition: "Poziția autoarei",
      dateExtracted: "Date extrase",
      pillCurrent: "la zi",
      lastExtract: "Ultima extragere",
      generatedAt: "Generat",
      sourceFile: "Fișier sursă",
      versionTitle: "Versiune & auto-detectare",
      detectedAuto: "Detectată automat",
      step1: "Scanează centralizator/v*/ și citari/v*/.",
      step2: "Alege versiunea numerică maximă comună.",
      step3: "Citește manifestul dashboard/data/version-manifest.json.",
      step4: "Încarcă CSV-urile versiunii; revine la datele încorporate pe file://.",
      sources: "Surse",
      sourceLinks: "{n} legături de citare",
      sourcePubs: "{n} publicații verificate",
      sourceNoCount: "verificare metadate",
      sourceManual: "import manual",
      footerNote: "Date din livrabilele versionate ale centralizatorului și raportului de citări.",
      footLeft: "Dashboard bibliografic · v1.0",
      footRight: "Auto-detectare versiune · date: centralizator {v} + citări {v}",
      loadError: "Datele nu au putut fi încărcate."
    },
    en: {
      appTitle: "Bibliographic dashboard",
      appSubtitle: "Gabriela Daniela Stamatie (Criveanu-Stamatie) · IBA Bucharest",
      updated: "Updated",
      redetect: "Re-detect",
      rescanning: "Scanning…",
      refreshData: "Refresh",
      detected: "Auto-detected version: {v}",
      notDetected: "Version not detected",
      rule: "rule: highest common numeric version",
      modeEmbedded: "embedded data (file://)",
      modeCsv: "CSV loaded at runtime",
      modeManifest: "manifest detected",
      noCommon: "no common version found",
      tabPublications: "Publications",
      tabCitations: "Citations",
      tabSynthesis: "Synthesis",
      exportCsv: "Export CSV",
      exportXlsx: "Download XLSX",
      search: "Search",
      pubSearchPh: "Title, author, DOI…",
      citSearchPh: "Citing work, author, DOI…",
      author: "Author / co-author",
      authorPh: "Author name…",
      year: "Year",
      citYear: "Citation year",
      allYears: "All years",
      type: "Type",
      allTypes: "All types",
      venue: "Journal",
      allVenues: "All journals",
      article: "Cited article",
      allArticles: "All articles",
      doiOnly: "DOI only",
      excludeSelf: "Exclude self-citations",
      reset: "Reset",
      chartsToggle: "Charts",
      pageSize: "Per page",
      removeFilter: "Remove filter",
      toastFresh: "Displayed data is up to date",
      toastUpdated: "Data updated",
      footDashboard: "Bibliographic dashboard",
      footCreated: "Created by",
      footWith: "with the help of",
      multiSelected: "{n} selected",
      pubFilterNote: "Filters apply instantly to the detected version.",
      citFilterNote: "Self-citations are highlighted; totals reflect the active filters.",
      pubTableTitle: "Central index",
      citTableTitle: "Citing works",
      colNr: "No.",
      colYear: "Year",
      colTitle: "Title",
      colVenue: "Journal",
      colType: "Type",
      colDoi: "DOI",
      colLink: "Link",
      colAuthors: "Authors",
      colVolume: "Vol/Issue",
      colCitations: "Citations",
      colSelf: "Self-citation",
      colNotes: "Notes",
      dateCitations: "Citations",
      pillStale: "needs update",
      synTitleFilter: "Article title",
      scholarExportTitle: "Google Scholar (export)",
      scholarExportCap: "Works from Scholar that are not in the central index yet.",
      synTitleFilterPh: "Filter by article title…",
      colArticle: "Art.",
      colCitYear: "Citation year",
      colCiting: "Citing work",
      firstPage: "First page",
      lastPage: "Last page",
      prevPage: "Previous page",
      nextPage: "Next page",
      pageLabel: "Page",
      prev: "Previous",
      next: "Next",
      pageOf: "Page {page} / {pages}",
      showingRange: "Showing {from}–{to} of {total}",
      noResults: "No records match the selected filters.",
      noResultsNote: "The active filters removed all results. Loosen the filters or reset them.",
      resultsFound: "{total} of {all}",
      copyLink: "Copy link",
      linkCopied: "Link copied",
      linkCopyFail: "Copy failed",
      noDoi: "no DOI",
      untitled: "Untitled",
      yes: "Yes",
      no: "No",
      pubPanelSub: "{n} records · {articles} articles · {doi} with DOI",
      citPanelSub: "{n} citing works · {links} links · {self} self-citations",
      kpiCiting: "Citing works",
      kpiLinks: "Citation links",
      kpiSelf: "Self-citations",
      kpiSelfLinks: "Self-citation links",
      kpiExternalLinks: "External citation links",
      kpiMaxYear: "Latest year",
      kpiHighlighted: "highlighted",
      kpiPublications: "Publications",
      kpiNoCitations: "Articles without citations",
      kpiExternalSub: "{n} external works",
      kpiLinksSub: "{n} external links",
      kpiMaxYearSub: "{n} links",
      synPubsSub: "{articles} articles + {other}",
      synWorksSub: "{n} external works",
      synLinksSub: "{n} external links",
      synMissingSub: "of {n}",
      pubByYear: "Publications per year",
      pubByYearCap: "Records by publication year (filtered).",
      pubTypes: "Publication types",
      pubTypesCap: "Distribution by type (filtered).",
      citByYear: "Citations per year",
      citByYearCap: "Citation links by citation year (filtered).",
      topCited: "Most cited articles",
      topCitedCap: "Citation links per article (filtered).",
      citTypes: "Citing work types",
      synPanelSub: "Indicators, article × citation-year matrix and data coverage.",
      synMatrix: "Article × citation-year matrix",
      pillAllData: "all data",
      synMatrixCap: "Cells count citation links; rows may total more than unique works.",
      matrixArticle: "Art.",
      matrixTotal: "Total",
      coverage: "Data coverage",
      coverageBadge: "{n} without citations",
      coverageCap: "Articles without citation links are marked separately.",
      coveragePartialBadge: "{n} partially verified",
      coveragePartialCap: "Articles without identifier, pending re-verification.",
      coveragePartialNote: "Not counted as \"without citations\" per the methodology.",
      qa: "QA & recommendations",
      qa1: "{links} links → {works} unique works; {self} self-citations ({external} external).",
      qa2: "Sample of 10 citing DOIs checked in Crossref: 10/10.",
      qa3: "The count is a minimum (OpenAlex); Scopus/WoS/Google Scholar are missing.",
      qa4: "Re-check: #5, #6, #8, #14, #19 and the 2026 articles.",
      pubDetails: "Article details",
      pubDetailsAuthors: "All authors",
      pubDetailsVolume: "Vol/Issue",
      pubDetailsPages: "Pages",
      pubDetailsIssn: "ISSN",
      pubDetailsPmid: "PMID/PMCID",
      pubDetailsSource: "Source",
      pubDetailsNotes: "Notes",
      pubDetailsCoverage: "Coverage",
      pubDetailsConfidence: "Confidence",
      pubDetailsCoverageNote: "Coverage note",
      pubDetailsLink: "Link",
      pubDetailsPosition: "Author position",
      dateExtracted: "Extracted data",
      pillCurrent: "current",
      lastExtract: "Last extraction",
      generatedAt: "Generated",
      sourceFile: "Source file",
      versionTitle: "Version & auto-detection",
      detectedAuto: "Auto-detected",
      step1: "Scan centralizator/v*/ and citari/v*/.",
      step2: "Pick the highest common numeric version.",
      step3: "Read the dashboard/data/version-manifest.json manifest.",
      step4: "Load the version CSVs; fall back to embedded data on file://.",
      sources: "Sources",
      sourceLinks: "{n} citation links",
      sourcePubs: "{n} verified publications",
      sourceNoCount: "metadata verification",
      sourceManual: "manual import",
      footerNote: "Data from the versioned central index and citation report deliverables.",
      footLeft: "Bibliographic dashboard · v1.0",
      footRight: "Version auto-detection · data: centralizator {v} + citari {v}",
      loadError: "The data could not be loaded."
    }
  };

  var TYPE_EN = { article: "Article", abstract: "Conference abstract", preprint: "Preprint", poster: "Poster", review: "Review", conference: "Conference paper", chapter: "Book chapter", thesis: "Thesis", other: "Other" };
  var TYPE_RO = { article: "Articol", abstract: "Abstract", preprint: "Preprint", poster: "Poster", review: "Review", conference: "Conferință", chapter: "Capitol de carte", thesis: "Teză", other: "Altele" };
  var TYPE_CLASS = { article: "pill-article", abstract: "pill-abstract", preprint: "pill-preprint", poster: "pill-other", review: "pill-review", conference: "pill-conf", chapter: "pill-chapter", thesis: "pill-chapter" };

  var PUB_TYPE_MAP = {
    "articol stiintific": "article",
    "articol stiintific (abstract)": "abstract",
    "preprint": "preprint",
    "poster nepublicat": "poster",
    "poster": "poster"
  };
  var CIT_TYPE_MAP = {
    "articol": "article",
    "review": "review",
    "lucrare de conferinta": "conference",
    "conference paper": "conference",
    "capitol de carte": "chapter",
    "book chapter": "chapter",
    "preprint": "preprint",
    "poster": "poster",
    "teza": "thesis",
    "thesis": "thesis"
  };

  var state = {
    lang: "ro",
    dark: false,
    data: null,
    manifest: null,
    version: null,
    sourceMode: "embedded",
    runtimeError: null,
    pubs: [],
    cits: [],
    stats: null,
    pubFilters: { q: "", author: "", year: [], type: [], venue: [], doiOnly: false },
    citFilters: { q: "", author: "", year: [], article: [], type: [], venue: [], doiOnly: false, excludeSelf: false },
    pubSort: { key: "citations", dir: "desc" },
    citSort: { key: "year", dir: "desc" },
    pubPage: 1,
    citPage: 1,
    pubPageSize: PUB_PAGE_SIZE,
    citPageSize: CIT_PAGE_SIZE,
    charts: {}
  };

  var TAB_IDS = { publicatii: "tab-publicatii", citari: "tab-citari", sinteza: "tab-sinteza" };
  var PUB_SORT_KEYS = ["id", "year", "title", "venue", "type", "citations"];
  var CIT_SORT_KEYS = ["id", "articleId", "year", "title", "venue", "type", "self"];
  var PUB_NUMERIC_SORTS = ["id", "year", "citations"];
  var CIT_NUMERIC_SORTS = ["id", "articleId", "year", "self"];
  var DEFAULT_PUB_SORT = { key: "id", dir: "asc" };
  var DEFAULT_CIT_SORT = { key: "year", dir: "desc" };

  function emptyUrlState() {
    return {
      tab: "",
      lang: "",
      pub: { q: "", author: "", year: [], type: [], venue: [], doiOnly: false },
      cit: { q: "", author: "", year: [], article: [], type: [], venue: [], doiOnly: false, excludeSelf: false },
      pubSort: null,
      citSort: null,
      pubPage: null,
      citPage: null
    };
  }

  function readUrlState() {
    var result = emptyUrlState();
    var params;
    try {
      params = new URLSearchParams(window.location.search || "");
    } catch (error) {
      return result;
    }
    function value(key) {
      var item = params.get(key);
      return item == null ? "" : item.trim();
    }
    function values(key) {
      var items = [];
      try { items = params.getAll(key); } catch (error) { items = []; }
      return items.map(function (item) { return String(item).trim(); }).filter(function (item) { return item !== ""; });
    }
    function flag(key) {
      return /^(1|true|yes)$/i.test(value(key));
    }
    function direction(key) {
      var dir = value(key).toLowerCase();
      return dir === "asc" || dir === "desc" ? dir : "";
    }
    function page(key) {
      var number = parseInt(value(key), 10);
      return isNaN(number) || number < 1 ? null : number;
    }
    function defaultDir(key, numeric) {
      return numeric.indexOf(key) !== -1 ? "desc" : "asc";
    }

    result.tab = value("tab").toLowerCase();
    result.lang = value("lang").toLowerCase();

    result.pub.q = value("pq");
    result.pub.author = value("pa");
    result.pub.year = values("py");
    result.pub.type = values("pt");
    result.pub.venue = values("pv");
    result.pub.doiOnly = flag("pd");
    result.pubPage = page("pp");
    var pubSortKey = value("psk").toLowerCase();
    if (PUB_SORT_KEYS.indexOf(pubSortKey) !== -1) {
      result.pubSort = { key: pubSortKey, dir: direction("psd") || defaultDir(pubSortKey, PUB_NUMERIC_SORTS) };
    }

    result.cit.q = value("cq");
    result.cit.author = value("ca");
    result.cit.year = values("cy");
    result.cit.article = values("ci");
    result.cit.venue = values("cv");
    result.cit.type = values("ct");
    result.cit.doiOnly = flag("cd");
    result.cit.excludeSelf = flag("cx");
    result.citPage = page("cp");
    var citSortKey = value("csk").toLowerCase();
    if (CIT_SORT_KEYS.indexOf(citSortKey) !== -1) {
      result.citSort = { key: citSortKey, dir: direction("csd") || defaultDir(citSortKey, CIT_NUMERIC_SORTS) };
    }

    return result;
  }

  function valueSet(values) {
    var set = {};
    values.forEach(function (item) {
      if (item != null && item !== "") set[String(item)] = true;
    });
    return set;
  }

  function applyUrlState(parsed) {
    var source = parsed || emptyUrlState();

    state.pubFilters = {
      q: source.pub.q || "",
      author: source.pub.author || "",
      year: [],
      type: [],
      venue: [],
      doiOnly: !!source.pub.doiOnly
    };
    state.citFilters = {
      q: source.cit.q || "",
      author: source.cit.author || "",
      year: [],
      article: [],
      type: [],
      venue: [],
      doiOnly: !!source.cit.doiOnly,
      excludeSelf: !!source.cit.excludeSelf
    };
    state.pubSort = source.pubSort
      ? { key: source.pubSort.key, dir: source.pubSort.dir }
      : { key: DEFAULT_PUB_SORT.key, dir: DEFAULT_PUB_SORT.dir };
    state.citSort = source.citSort
      ? { key: source.citSort.key, dir: source.citSort.dir }
      : { key: DEFAULT_CIT_SORT.key, dir: DEFAULT_CIT_SORT.dir };
    state.pubPage = source.pubPage || 1;
    state.citPage = source.citPage || 1;

    if (source.lang === "ro" || source.lang === "en") state.lang = source.lang;
    setActiveTab(TAB_IDS[source.tab] ? source.tab : "publicatii");

    var pubYears = valueSet(state.pubs.map(function (pub) { return pub.year; }));
    state.pubFilters.year = (source.pub.year || []).filter(function (v) { return pubYears[v]; });
    var pubTypes = valueSet(state.pubs.map(function (pub) { return pub.typeCode; }));
    state.pubFilters.type = (source.pub.type || []).filter(function (v) { return pubTypes[v]; });
    var pubVenues = valueSet(state.pubs.map(function (pub) { return pub.venue; }));
    state.pubFilters.venue = (source.pub.venue || []).filter(function (v) { return pubVenues[v]; });

    var citYears = valueSet(state.cits.map(function (citation) { return citation.year; }));
    state.citFilters.year = (source.cit.year || []).filter(function (v) { return citYears[v]; });
    var citTypes = valueSet(state.cits.map(function (citation) { return citation.typeCode; }));
    state.citFilters.type = (source.cit.type || []).filter(function (v) { return citTypes[v]; });
    var citVenues = valueSet(state.cits.map(function (citation) { return citation.venue; }));
    state.citFilters.venue = (source.cit.venue || []).filter(function (v) { return citVenues[v]; });
    var citedIds = valueSet(state.pubs.filter(function (pub) { return pub._citations > 0; })
      .map(function (pub) { return pub.id; }));
    state.citFilters.article = (source.cit.article || []).filter(function (v) { return citedIds[v]; });
  }

  function setActiveTab(tab) {
    var input = document.getElementById(TAB_IDS[tab]);
    if (input) input.checked = true;
  }

  function currentTab() {
    var inputs = document.querySelectorAll(".tab-input");
    for (var index = 0; index < inputs.length; index += 1) {
      if (inputs[index].checked) {
        var id = inputs[index].id;
        for (var key in TAB_IDS) {
          if (Object.prototype.hasOwnProperty.call(TAB_IDS, key) && TAB_IDS[key] === id) return key;
        }
      }
    }
    return "publicatii";
  }

  function writeUrlState(mode) {
    var params = new URLSearchParams();
    var tab = currentTab();
    if (tab && tab !== "publicatii") params.set("tab", tab);
    if (state.lang === "en") params.set("lang", "en");

    function appendAll(key, arr) { (arr || []).forEach(function (v) { params.append(key, v); }); }
    var pub = state.pubFilters;
    if (pub.q) params.set("pq", pub.q);
    if (pub.author) params.set("pa", pub.author);
    appendAll("py", pub.year);
    appendAll("pt", pub.type);
    appendAll("pv", pub.venue);
    if (pub.doiOnly) params.set("pd", "1");
    if (state.pubSort.key !== DEFAULT_PUB_SORT.key || state.pubSort.dir !== DEFAULT_PUB_SORT.dir) {
      params.set("psk", state.pubSort.key);
      params.set("psd", state.pubSort.dir);
    }
    if (state.pubPage > 1) params.set("pp", String(state.pubPage));

    var cit = state.citFilters;
    if (cit.q) params.set("cq", cit.q);
    if (cit.author) params.set("ca", cit.author);
    appendAll("cy", cit.year);
    appendAll("ci", cit.article);
    appendAll("cv", cit.venue);
    appendAll("ct", cit.type);
    if (cit.doiOnly) params.set("cd", "1");
    if (cit.excludeSelf) params.set("cx", "1");
    if (state.citSort.key !== DEFAULT_CIT_SORT.key || state.citSort.dir !== DEFAULT_CIT_SORT.dir) {
      params.set("csk", state.citSort.key);
      params.set("csd", state.citSort.dir);
    }
    if (state.citPage > 1) params.set("cp", String(state.citPage));

    var query = params.toString();
    var hash = window.location.hash || "";
    var next = window.location.pathname + (query ? "?" + query : "") + hash;
    var current = window.location.pathname + window.location.search + hash;
    if (next === current) return;
    try {
      if (mode === "push") {
        window.history.pushState({ dashboard: true }, "", next);
      } else {
        window.history.replaceState({ dashboard: true }, "", next);
      }
    } catch (error) {
      /* history API can be blocked on file://; the view keeps working, only the URL stays unsynced */
    }
  }

  function onUrlPopState() {
    if (!state.stats) return;
    applyUrlState(readUrlState());
    renderAll();
    writeUrlState("replace");
  }

  function $(id) { return document.getElementById(id); }

  function fold(value) {
    return String(value == null ? "" : value)
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .replace(/\s+/g, " ")
      .trim();
  }

  function t(key, vars) {
    var table = I18N[state.lang] || I18N.ro;
    var text = table[key] != null ? table[key] : (I18N.ro[key] != null ? I18N.ro[key] : key);
    if (vars) {
      Object.keys(vars).forEach(function (name) {
        text = text.split("{" + name + "}").join(String(vars[name]));
      });
    }
    return text;
  }

  function fmt(value) {
    if (value == null || isNaN(value)) return "—";
    try {
      return new Intl.NumberFormat(state.lang === "ro" ? "ro-RO" : "en-GB").format(value);
    } catch (error) {
      return String(value);
    }
  }

  function esc(value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch];
    });
  }

  function showLoading() {
    var overlay = document.createElement("div");
    overlay.className = "loading-overlay";
    overlay.innerHTML = '<div class="spinner"></div><p>Se încarcă datele…</p>';
    document.body.appendChild(overlay);
  }

  function hideLoading() {
    var overlay = document.querySelector(".loading-overlay");
    if (overlay) overlay.remove();
  }

  var copyMsgTimer = null;
  function copyCurrentLink(msgId) {
    var msg = document.getElementById(msgId);
    var done = function (ok) {
      if (!msg) return;
      msg.textContent = t(ok ? "linkCopied" : "linkCopyFail");
      if (copyMsgTimer) clearTimeout(copyMsgTimer);
      copyMsgTimer = setTimeout(function () { msg.textContent = ""; }, 2500);
    };
    var url = window.location.href;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(function () { done(true); }, function () { done(false); });
      return;
    }
    var ta = document.createElement("textarea");
    ta.value = url;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    ta.remove();
    done(ok);
  }

  function short(value, length) {
    var text = String(value == null ? "" : value);
    return text.length > length ? text.slice(0, length - 1) + "…" : text;
  }

  function clean(value) {
    return String(value == null ? "" : value).replace(/\s+/g, " ").trim();
  }

  function parseIntSafe(value) {
    var match = String(value == null ? "" : value).match(/-?\d+/);
    return match ? parseInt(match[0], 10) : null;
  }

  function splitAuthors(value) {
    return String(value == null ? "" : value).split(";").map(clean).filter(Boolean);
  }

  function normalizeDoi(value) {
    var match = String(value == null ? "" : value).match(/10\.\d{4,9}\/[^\s;]+/i);
    if (!match) return "";
    return match[0].replace(/[.,);\]}>]+$/, "").toLowerCase();
  }

  function normalizeLink(value, doi) {
    var text = clean(value);
    if (!text) return doi ? "https://doi.org/" + doi : "";
    if (/^10\./i.test(text)) return "https://doi.org/" + text;
    if (/^https?:\/\//i.test(text)) return text;
    return "";
  }

  function typeCodeFor(label, map) {
    return map[fold(label)] || "other";
  }

  function typeLabel(code, fallback) {
    var map = state.lang === "en" ? TYPE_EN : TYPE_RO;
    return map[code] || fallback || code;
  }

  function typePill(code) {
    return TYPE_CLASS[code] || "pill-other";
  }

  function parseArticleIds(value) {
    var ids = [];
    String(value == null ? "" : value).split(/[,;/]/).forEach(function (part) {
      var parsed = parseIntSafe(part);
      if (parsed != null && ids.indexOf(parsed) === -1) ids.push(parsed);
    });
    return ids;
  }

  function isSelfCitation(context, authors) {
    var foldedAuthors = (authors || []).map(fold).join(" ; ");
    if (foldedAuthors.indexOf("stamatie") !== -1) return true;
    return /auto-?citare\s*[:\-]?\s*(da|yes|true)/.test(fold(context));
  }

  function normalizePublications(rows) {
    return rows.map(function (row, index) {
      var doi = normalizeDoi(row["DOI"]);
      var pub = {
        id: parseIntSafe(row["Nr."]) != null ? parseIntSafe(row["Nr."]) : index + 1,
        year: parseIntSafe(row["An"]),
        typeCode: typeCodeFor(row["Tip"], PUB_TYPE_MAP),
        typeLabel: clean(row["Tip"]),
        title: clean(row["Titlu"]),
        venue: clean(row["Revistă / Publicație"]),
        volume: clean(row["Volum (Issue)"]),
        pages: clean(row["Pagini / Nr. articol"]),
        doi: doi,
        link: normalizeLink(row["Link"], doi),
        authors: splitAuthors(row["Toți autorii"]),
        coauthors: splitAuthors(row["Co-autori (fără G. D. Stamatie)"]),
        position: clean(row["Poziția autoarei"]),
        issn: clean(row["ISSN"]),
        pmid: clean(row["PMID / PMCID"]),
        source: clean(row["Sursa verificării"]),
        notes: clean(row["Note / incertitudine"])
      };
      if (row["Stare acoperire citări"] !== undefined || row["Citări găsite (v4)"] !== undefined) {
        pub.citationsFound = parseIntSafe(row["Citări găsite (v4)"]);
        pub.verifiedSources = splitAuthors(row["Surse verificate (citări)"]);
        pub.coverageStatus = clean(row["Stare acoperire citări"]);
        pub.confidence = clean(row["Încredere agregată"]);
        pub.coverageNote = clean(row["Notă acoperire"]);
      }
      return pub;
    });
  }

  function normalizeCitations(rows, publications) {
    var years = {};
    var titles = {};
    publications.forEach(function (pub) {
      years[pub.id] = pub.year;
      titles[pub.id] = pub.title;
    });

    return rows.map(function (row, index) {
      var citation;
      if (Object.prototype.hasOwnProperty.call(row, "Articol (ID)")) {
        var ids = parseArticleIds(row["Articol (ID)"]);
        var doi = normalizeDoi(row["DOI citare"]);
        var authors = splitAuthors(row["Autori citatori"]);
        var context = clean(row["Context / Observații"]);
        citation = {
          id: parseIntSafe(row["Nr."]) != null ? parseIntSafe(row["Nr."]) : index + 1,
          articleId: ids.length ? ids[0] : null,
          articleIds: ids,
          articleTitle: clean(row["Titlu articol"]),
          articleYear: parseIntSafe(row["An publicație"]),
          year: parseIntSafe(row["An citare"]),
          title: clean(row["Lucrare citată"]),
          authors: authors,
          venue: clean(row["Revistă / Eveniment"]),
          doi: doi,
          link: normalizeLink(row["Link"], doi),
          typeCode: typeCodeFor(row["Tip citare"], CIT_TYPE_MAP),
          typeLabel: clean(row["Tip citare"]),
          selfCitation: isSelfCitation(context, authors),
          context: context,
          source: clean(row["Sursă verificare"])
        };
      } else {
        var v1ids = parseArticleIds(row["Articol citat (nr.)"]);
        var v1authors = splitAuthors(row["Autori"]);
        var combined = clean(row["DOI / Link"]);
        var v1doi = normalizeDoi(combined);
        var selfFlag = clean(row["Auto-citare"]);
        citation = {
          id: parseIntSafe(row["Nr. crt."]) != null ? parseIntSafe(row["Nr. crt."]) : index + 1,
          articleId: v1ids.length ? v1ids[0] : null,
          articleIds: v1ids,
          articleTitle: clean(row["Articol citat – titlu"]),
          articleYear: v1ids.length ? (years[v1ids[0]] != null ? years[v1ids[0]] : null) : null,
          year: parseIntSafe(row["An citare"]),
          title: clean(row["Titlu lucrare citantă"]),
          authors: v1authors,
          venue: clean(row["Revistă / Conferință"]),
          doi: v1doi,
          link: normalizeLink(combined, v1doi),
          typeCode: typeCodeFor(row["Tip"], CIT_TYPE_MAP),
          typeLabel: clean(row["Tip"]),
          selfCitation: isSelfCitation([selfFlag, row["Note"]].join(" "), v1authors),
          context: clean([selfFlag ? "Auto-citare: " + selfFlag : "", row["Note"]].join(" · ")),
          source: clean(row["Sursă"])
        };
      }

      if (!citation.articleTitle && citation.articleId != null) {
        citation.articleTitle = titles[citation.articleId] || "";
      }
      if (citation.articleYear == null && citation.articleId != null && years[citation.articleId] != null) {
        citation.articleYear = years[citation.articleId];
      }
      return citation;
    });
  }

  function parseCsv(text) {
    var content = String(text || "").replace(/^\uFEFF/, "");
    var firstLine = content.split(/\r?\n/)[0] || "";
    var delimiter = (firstLine.split(";").length >= firstLine.split(",").length) ? ";" : ",";
    var rows = [];
    var row = [];
    var field = "";
    var inQuotes = false;

    for (var i = 0; i < content.length; i += 1) {
      var ch = content.charAt(i);
      if (inQuotes) {
        if (ch === '"') {
          if (content.charAt(i + 1) === '"') {
            field += '"';
            i += 1;
          } else {
            inQuotes = false;
          }
        } else {
          field += ch;
        }
      } else if (ch === '"') {
        inQuotes = true;
      } else if (ch === delimiter) {
        row.push(field);
        field = "";
      } else if (ch === "\n") {
        row.push(field);
        field = "";
        rows.push(row);
        row = [];
      } else if (ch === "\r") {
        if (content.charAt(i + 1) !== "\n") {
          row.push(field);
          field = "";
          rows.push(row);
          row = [];
        }
      } else {
        field += ch;
      }
    }
    if (field.length || row.length) {
      row.push(field);
      rows.push(row);
    }
    if (!rows.length) return [];
    var header = rows.shift().map(function (name) { return clean(name); });
    return rows.filter(function (cells) {
      return cells.some(function (cell) { return clean(cell) !== ""; });
    }).map(function (cells) {
      var record = {};
      header.forEach(function (name, index) {
        record[name] = clean(cells[index]);
      });
      return record;
    });
  }

  function fetchJson(url) {
    return fetch(url, { cache: "no-store" }).then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status + " for " + url);
      return response.json();
    });
  }

  function fetchCsv(url) {
    return fetch(url, { cache: "no-store" }).then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status + " for " + url);
      return response.text();
    }).then(parseCsv);
  }

  function latestVersion(versions) {
    return versions.slice().sort(function (a, b) {
      var na = parseIntSafe(a);
      var nb = parseIntSafe(b);
      return (nb || 0) - (na || 0);
    })[0] || null;
  }

  function loadData() {
    var embedded = window.DASHBOARD_DATA;
    if (!embedded || !embedded.datasets) {
      return Promise.reject(new Error("window.DASHBOARD_DATA is missing; run scripts/build_dashboard_data.py"));
    }

    var manifest = embedded.manifest || null;
    var version = manifest && manifest.latest && manifest.latest.common
      ? manifest.latest.common
      : latestVersion(Object.keys(embedded.datasets));
    var datasets = embedded.datasets;
    var mode = "embedded";
    var runtimeError = null;

    var embeddedManifest = embedded.manifest || null;
    var embeddedVersion = embeddedManifest && embeddedManifest.latest && embeddedManifest.latest.common
      ? embeddedManifest.latest.common
      : latestVersion(Object.keys(embedded.datasets));

    var canFetch = location.protocol === "http:" || location.protocol === "https:";
    var remote = canFetch
      ? fetchJson("data/version-manifest.json").then(function (remoteManifest) {
        if (!remoteManifest || !remoteManifest.latest || !remoteManifest.latest.common) {
          return null;
        }
        var remoteVersion = remoteManifest.latest.common;
        var info = (remoteManifest.versions || []).filter(function (item) {
          return item.version === remoteVersion;
        })[0];
        if (!info || !info.centralizator || !info.citari || !info.centralizator.csv || !info.citari.csv) {
          return null;
        }
        return Promise.all([
          fetchCsv(info.centralizator.csv),
          fetchCsv(info.citari.csv)
        ]).then(function (results) {
          var pubs = normalizePublications(results[0]);
          var cits = normalizeCitations(results[1], pubs);
          if (!pubs.length) return null;
          var next = Object.assign({}, datasets);
          next[remoteVersion] = { publications: pubs, citations: cits };
          datasets = next;
          manifest = remoteManifest;
          version = remoteVersion;
          mode = "csv";
          return null;
        });
      }).catch(function (error) {
        runtimeError = error;
        manifest = embeddedManifest;
        version = embeddedVersion;
        mode = "embedded";
        console.warn("[dashboard] runtime CSV load failed; using embedded data", error);
        return null;
      })
      : Promise.resolve(null);

    return remote.then(function () {
      var dataset = datasets[version] || embedded.datasets[version];
      if (!dataset) throw new Error("No dataset found for version " + version);
      state.data = embedded;
      state.manifest = manifest;
      state.version = version;
      state.sourceMode = mode;
      state.runtimeError = runtimeError;
      state.pubs = dataset.publications.map(function (pub) { return Object.assign({}, pub); });
      state.cits = dataset.citations.map(function (citation) { return Object.assign({}, citation); });
      computeDerived();
    });
  }

  function computeDerived() {
    var counts = {};
    state.cits.forEach(function (citation) {
      var ids = Array.isArray(citation.articleIds) && citation.articleIds.length
        ? citation.articleIds.slice()
        : (citation.articleId != null ? [citation.articleId] : []);
      citation._articleIds = ids;
      ids.forEach(function (id) {
        counts[id] = (counts[id] || 0) + 1;
      });
    });
    state.pubs.forEach(function (pub) {
      pub._citations = counts[pub.id] || 0;
    });
    state.counts = counts;

    var links = state.cits.reduce(function (sum, citation) {
      return sum + citation._articleIds.length;
    }, 0);
    var selfCits = state.cits.filter(function (citation) { return citation.selfCitation; });
    state.stats = {
      publications: state.pubs.length,
      works: state.cits.length,
      links: links,
      self: selfCits.length,
      selfLinks: selfCits.reduce(function (sum, citation) {
        return sum + citation._articleIds.length;
      }, 0),
      missing: state.pubs.filter(function (pub) { return !pub._citations; }).length
    };
  }

  function formatDate(value, withTime) {
    if (!value) return "—";
    var dateOnly = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(value));
    var pad = function (number) { return String(number).padStart(2, "0"); };
    if (dateOnly) {
      return state.lang === "ro"
        ? dateOnly[3] + "." + dateOnly[2] + "." + dateOnly[1]
        : dateOnly[1] + "-" + dateOnly[2] + "-" + dateOnly[3];
    }
    var date = new Date(value);
    if (isNaN(date.getTime())) return String(value);
    var datePart = state.lang === "ro"
      ? pad(date.getDate()) + "." + pad(date.getMonth() + 1) + "." + date.getFullYear()
      : date.getFullYear() + "-" + pad(date.getMonth() + 1) + "-" + pad(date.getDate());
    return withTime ? datePart + " " + pad(date.getHours()) + ":" + pad(date.getMinutes()) : datePart;
  }

  function applyI18n() {
    document.documentElement.lang = state.lang;
    document.querySelectorAll("[data-i18n]").forEach(function (element) {
      element.textContent = t(element.getAttribute("data-i18n"));
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach(function (element) {
      element.setAttribute("placeholder", t(element.getAttribute("data-i18n-placeholder")));
    });
    document.querySelectorAll("[data-i18n-title]").forEach(function (element) {
      element.setAttribute("title", t(element.getAttribute("data-i18n-title")));
    });
    document.querySelectorAll("[data-i18n-aria]").forEach(function (element) {
      element.setAttribute("aria-label", t(element.getAttribute("data-i18n-aria")));
    });
    document.querySelectorAll(".lang-btn").forEach(function (button) {
      button.classList.toggle("is-active", button.getAttribute("data-lang") === state.lang);
    });
    document.querySelectorAll(".theme-btn").forEach(function (button) {
      button.classList.toggle("is-active", button.getAttribute("data-theme-value") === (state.dark ? "dark" : "light"));
    });
    document.title = t("appTitle") + " · Gabriela Daniela Stamatie";
  }

  function applyTheme() {
    try {
      document.documentElement.setAttribute("data-theme", state.dark ? "dark" : "light");
    } catch (error) { /* ignore */ }
  }

  function fillSelect(multi, allLabel, values, current, labelFn) {
    if (!multi) return;
    var panel = multi.querySelector(".multi-panel");
    var currentArr = Array.isArray(current)
      ? current.map(String)
      : (current == null || current === "" ? [] : [String(current)]);
    panel.innerHTML = values.map(function (value) {
      var v = String(value);
      return '<label class="multi-item"><input type="checkbox" value="' + esc(v) + '"' +
        (currentArr.indexOf(v) !== -1 ? " checked" : "") + ">" +
        esc(labelFn ? labelFn(value) : v) + "</label>";
    }).join("");
    multi._allLabel = allLabel;
    updateMultiLabel(multi);
  }

  function selectedValues(multi) {
    if (!multi) return [];
    return Array.from(multi.querySelectorAll(".multi-panel input:checked"))
      .map(function (input) { return input.value; });
  }

  function setMultiSelect(multi, arr) {
    if (!multi) return;
    var chosen = {};
    (arr || []).forEach(function (value) { chosen[String(value)] = true; });
    multi.querySelectorAll(".multi-panel input").forEach(function (input) {
      input.checked = !!chosen[input.value];
    });
    updateMultiLabel(multi);
  }

  function updateMultiLabel(multi) {
    var label = multi.querySelector(".multi-label");
    if (!label) return;
    var checked = multi.querySelectorAll(".multi-panel input:checked");
    if (!checked.length) {
      label.textContent = multi._allLabel || "";
    } else if (checked.length === 1) {
      label.textContent = checked[0].closest(".multi-item").textContent.trim();
    } else {
      label.textContent = t("multiSelected", { n: checked.length });
    }
  }

  function closeAllMulti() {
    document.querySelectorAll(".multi-panel").forEach(function (panel) { panel.hidden = true; });
    document.querySelectorAll(".multi-btn").forEach(function (button) {
      button.setAttribute("aria-expanded", "false");
    });
  }

  function positionMultiPanel(multi) {
    var button = multi.querySelector(".multi-btn");
    var panel = multi.querySelector(".multi-panel");
    var rect = button.getBoundingClientRect();
    panel.style.left = Math.round(rect.left) + "px";
    panel.style.top = Math.round(rect.bottom + 4) + "px";
    panel.style.minWidth = Math.round(rect.width) + "px";
  }

  function bindMulti(id, onChange) {
    var multi = $(id);
    var button = multi.querySelector(".multi-btn");
    var panel = multi.querySelector(".multi-panel");
    button.addEventListener("click", function (event) {
      event.stopPropagation();
      var wasHidden = panel.hidden;
      closeAllMulti();
      if (wasHidden) positionMultiPanel(multi);
      panel.hidden = !wasHidden;
      button.setAttribute("aria-expanded", String(wasHidden));
    });
    panel.addEventListener("click", function (event) { event.stopPropagation(); });
    panel.addEventListener("change", function () {
      updateMultiLabel(multi);
      onChange();
    });
  }

  function uniqueSorted(values) {
    return Array.from(new Set(values.filter(function (value) {
      return value != null && value !== "";
    }))).sort(function (a, b) {
      return String(a).localeCompare(String(b), state.lang === "ro" ? "ro" : "en", { sensitivity: "base" });
    });
  }

  function populateFilters() {
    var pubYears = Array.from(new Set(state.pubs.map(function (pub) { return pub.year; }).filter(function (year) {
      return year != null;
    }))).sort(function (a, b) { return a - b; });

    var citYears = Array.from(new Set(state.cits.map(function (citation) { return citation.year; }).filter(function (year) {
      return year != null;
    }))).sort(function (a, b) { return a - b; });

    var pubTypes = uniqueSorted(state.pubs.map(function (pub) { return pub.typeCode; }));
    var citTypes = uniqueSorted(state.cits.map(function (citation) { return citation.typeCode; }));
    var pubVenues = uniqueSorted(state.pubs.map(function (pub) { return pub.venue; }));
    var citVenues = uniqueSorted(state.cits.map(function (citation) { return citation.venue; }));

    var citedArticles = state.pubs.filter(function (pub) { return pub._citations > 0; })
      .sort(function (a, b) { return b._citations - a._citations || a.id - b.id; });

    fillSelect($("pubYear"), t("allYears"), pubYears, state.pubFilters.year);
    fillSelect($("pubType"), t("allTypes"), pubTypes, state.pubFilters.type, function (code) {
      return typeLabel(code);
    });
    fillSelect($("pubVenue"), t("allVenues"), pubVenues, state.pubFilters.venue);

    fillSelect($("citYear"), t("allYears"), citYears, state.citFilters.year);
    fillSelect($("citArticle"), t("allArticles"), citedArticles.map(function (pub) { return pub.id; }), state.citFilters.article, function (id) {
      var pub = state.pubs.filter(function (item) { return item.id === Number(id); })[0];
      return "#" + id + " · " + short(pub ? pub.title : "", 34);
    });
    fillSelect($("citVenue"), t("allVenues"), citVenues, state.citFilters.venue);
    fillSelect($("citType"), t("allTypes"), citTypes, state.citFilters.type, function (code) {
      return typeLabel(code);
    });

    var names = new Set();
    state.pubs.forEach(function (pub) {
      (pub.authors || []).forEach(function (author) { names.add(author); });
    });
    state.cits.forEach(function (citation) {
      (citation.authors || []).forEach(function (author) { names.add(author); });
    });
    $("authorsList").innerHTML = Array.from(names).sort(function (a, b) {
      return a.localeCompare(b, state.lang === "ro" ? "ro" : "en", { sensitivity: "base" });
    }).map(function (name) {
      return '<option value="' + esc(name) + '"></option>';
    }).join("");
  }

  function setPageSizeButtons(id, size) {
    Array.from($(id).querySelectorAll("button")).forEach(function (button) {
      button.setAttribute("aria-pressed", String(Number(button.getAttribute("data-size")) === size));
    });
  }

  function syncControls() {
    setPageSizeButtons("pubPageSize", state.pubPageSize);
    setPageSizeButtons("citPageSize", state.citPageSize);
    $("pubSearch").value = state.pubFilters.q;
    $("pubAuthor").value = state.pubFilters.author;
    setMultiSelect($("pubYear"), state.pubFilters.year);
    setMultiSelect($("pubType"), state.pubFilters.type);
    setMultiSelect($("pubVenue"), state.pubFilters.venue);
    $("pubDoiOnly").checked = !!state.pubFilters.doiOnly;

    $("citSearch").value = state.citFilters.q;
    $("citAuthor").value = state.citFilters.author;
    setMultiSelect($("citYear"), state.citFilters.year);
    setMultiSelect($("citArticle"), state.citFilters.article);
    setMultiSelect($("citVenue"), state.citFilters.venue);
    setMultiSelect($("citType"), state.citFilters.type);
    $("citDoiOnly").checked = !!state.citFilters.doiOnly;
    $("citExcludeSelf").checked = !!state.citFilters.excludeSelf;
  }

  function matchQuery(query, parts) {
    if (!query) return true;
    return fold(parts.join(" ")).indexOf(fold(query)) !== -1;
  }

  function matchAuthor(authors, query) {
    if (!query) return true;
    var needle = fold(query);
    return (authors || []).some(function (author) {
      return fold(author).indexOf(needle) !== -1;
    });
  }

  function getFilteredPubs() {
    var filters = state.pubFilters;
    return state.pubs.filter(function (pub) {
      if (filters.year.length && filters.year.indexOf(String(pub.year)) === -1) return false;
      if (filters.type.length && filters.type.indexOf(pub.typeCode) === -1) return false;
      if (filters.venue.length && filters.venue.indexOf(pub.venue) === -1) return false;
      if (filters.doiOnly && !pub.doi) return false;
      if (!matchAuthor(pub.authors, filters.author)) return false;
      return matchQuery(filters.q, [pub.title, pub.venue, pub.doi, (pub.authors || []).join(" "), pub.notes, pub.source]);
    });
  }

  function getFilteredCits() {
    var filters = state.citFilters;
    return state.cits.filter(function (citation) {
      if (filters.year.length && filters.year.indexOf(String(citation.year)) === -1) return false;
      if (filters.article.length && !citation._articleIds.some(function (id) { return filters.article.indexOf(String(id)) !== -1; })) return false;
      if (filters.type.length && filters.type.indexOf(citation.typeCode) === -1) return false;
      if (filters.venue.length && filters.venue.indexOf(citation.venue) === -1) return false;
      if (filters.doiOnly && !citation.doi) return false;
      if (filters.excludeSelf && citation.selfCitation) return false;
      if (!matchAuthor(citation.authors, filters.author)) return false;
      return matchQuery(filters.q, [citation.title, citation.articleTitle, citation.venue, citation.doi, (citation.authors || []).join(" "), citation.context, citation.source]);
    });
  }

  function compareValues(a, b) {
    if (a == null && b == null) return 0;
    if (a == null) return 1;
    if (b == null) return -1;
    if (typeof a === "number" && typeof b === "number") return a - b;
    return String(a).localeCompare(String(b), state.lang === "ro" ? "ro" : "en", { sensitivity: "base" });
  }

  function pubComparator() {
    var sort = state.pubSort;
    return function (a, b) {
      var left;
      var right;
      if (sort.key === "citations") {
        left = a._citations;
        right = b._citations;
      } else if (sort.key === "type") {
        left = typeLabel(a.typeCode);
        right = typeLabel(b.typeCode);
      } else {
        left = a[sort.key];
        right = b[sort.key];
      }
      var result = compareValues(left, right);
      if (result === 0) result = compareValues(a.id, b.id);
      return sort.dir === "desc" ? -result : result;
    };
  }

  function citComparator() {
    var sort = state.citSort;
    return function (a, b) {
      var left;
      var right;
      if (sort.key === "self") {
        left = a.selfCitation ? 1 : 0;
        right = b.selfCitation ? 1 : 0;
      } else if (sort.key === "type") {
        left = typeLabel(a.typeCode);
        right = typeLabel(b.typeCode);
      } else if (sort.key === "articleId") {
        left = a._articleIds.length ? Math.min.apply(null, a._articleIds) : null;
        right = b._articleIds.length ? Math.min.apply(null, b._articleIds) : null;
      } else {
        left = a[sort.key];
        right = b[sort.key];
      }
      var result = compareValues(left, right);
      if (result === 0) result = compareValues(a.id, b.id);
      return sort.dir === "desc" ? -result : result;
    };
  }

  function updateSortIndicators(table, sort) {
    table.querySelectorAll("th[data-sort]").forEach(function (header) {
      if (header.getAttribute("data-sort") === sort.key) {
        header.setAttribute("aria-sort", sort.dir === "asc" ? "ascending" : "descending");
      } else {
        header.removeAttribute("aria-sort");
      }
    });
  }

  function pubRowHtml(pub) {
    var citations = pub._citations || 0;
    var doi = pub.doi
      ? '<a class="doi" href="' + esc(pub.link || ("https://doi.org/" + pub.doi)) + '" target="_blank" rel="noopener">' + esc(pub.doi) + "</a>"
      : '<span class="muted">' + esc(t("noDoi")) + "</span>";
    var link = pub.link
      ? '<a class="ext-link" href="' + esc(pub.link) + '" target="_blank" rel="noopener" title="' + esc(t("pubDetailsLink")) + '">🔗</a>'
      : "";
    var volume = esc(pub.volume || pub.pages || "—");
    var coverageClass = pub.coverageStatus === "zero confirmat" ? "pill-warn" : pub.coverageStatus === "parțial verificat - fără identificator" ? "pill-neutral" : "";
    var coverageLabel = pub.coverageStatus === "zero confirmat" ? t("kpiNoCitations") : pub.coverageStatus === "parțial verificat - fără identificator" ? t("coveragePartialBadge", { n: "?" }) : "";
    var citationCell = '<td class="num ' + (citations ? "strong" : "muted") + '">' + fmt(citations) + "</td>";
    var notesText = [pub.notes, coverageLabel].filter(function (part) { return part; }).join(" · ") || "—";
    var detailRows = [
      esc(pub.title || t("untitled")),
      pub.year == null ? "—" : esc(pub.year),
      esc(pub.venue || "—"),
      esc(pub.typeLabel || "—"),
      esc(pub.doi || "—"),
      esc(pub.link || "—"),
      esc((pub.authors || []).join("; ") || "—"),
      esc(pub.coauthors && pub.coauthors.length ? "(co: " + pub.coauthors.join("; ") + ")" : ""),
      esc(pub.position || "—"),
      esc(pub.volume || "—"),
      esc(pub.pages || "—"),
      esc(pub.issn || "—"),
      esc(pub.pmid || "—"),
      esc(pub.source || "—"),
      esc(pub.notes || "—"),
      esc(pub.coverageStatus || "—"),
      esc(pub.confidence || "—"),
      esc(pub.coverageNote || "—")
    ].map(function (text, idx) {
      var labels = [
        t("colTitle"), t("colYear"), t("colVenue"), t("colType"), t("colDoi"), t("pubDetailsLink"),
        t("pubDetailsAuthors"), "", t("pubDetailsPosition"), t("pubDetailsVolume"), t("pubDetailsPages"),
        t("pubDetailsIssn"), t("pubDetailsPmid"), t("pubDetailsSource"), t("pubDetailsNotes"),
        t("pubDetailsCoverage"), t("pubDetailsConfidence"), t("pubDetailsCoverageNote")
      ];
      var label = labels[idx];
      if (!label && idx === 7) label = "Co-autori";
      var valueHtml = idx === 5 && pub.link
        ? '<a href="' + esc(pub.link) + '" target="_blank" rel="noopener">' + esc(pub.link) + "</a>"
        : text;
      return '<div class="detail-row"><span class="detail-label">' + label + '</span><span class="detail-value">' + valueHtml + "</span></div>";
    }).join("");
    return "<tr class=\"pub-main\" data-id=\"" + esc(pub.id) + "\" aria-expanded=\"false\">" +
      '<td class="num"><span class="pub-expand-icon">▸</span>' + esc(pub.id) + "</td>" +
      '<td class="num">' + esc(pub.year == null ? "—" : pub.year) + "</td>" +
      '<td class="cell-title">' + esc(pub.title || t("untitled")) + "</td>" +
      "<td>" + esc(pub.venue || "—") + "</td>" +
      "<td>" + esc(pub.volume || "—") + "</td>" +
      '<td><span class="pill ' + typePill(pub.typeCode) + '">' + esc(typeLabel(pub.typeCode, pub.typeLabel)) + "</span></td>" +
      "<td>" + doi + "</td>" +
      '<td class="cell-authors" title="' + esc((pub.authors || []).join("; ")) + '">' + esc(authorsShort(pub.authors)) + "</td>" +
      citationCell +
      '<td class="cell-notes">' + esc(notesText) + "</td>" +
      "<td>" + link + "</td>" +
      "</tr>" +
      "<tr class=\"pub-detail\" data-id=\"" + esc(pub.id) + "\" style=\"display:none\"><td colspan=\"11\" class=\"detail-cell\">" +
      '<div class="detail-panel">' + detailRows + "</div>" +
      "</td></tr>";
  }

  function authorsShort(authors) {
    var list = authors || [];
    if (!list.length) return "—";
    var shown = list.slice(0, 3).map(esc).join("; ");
    return shown + (list.length > 3 ? " …" : "");
  }

  function citRowHtml(citation) {
    var ids = citation._articleIds.length ? citation._articleIds.join(", ") : "—";
    var doi = citation.doi
      ? '<a class="doi" href="' + esc(citation.link || ("https://doi.org/" + citation.doi)) + '" target="_blank" rel="noopener">' + esc(short(citation.doi, 24)) + "</a>"
      : '<span class="muted">' + esc(t("noDoi")) + "</span>";
    var articleTip = citation.articleTitle ? ' title="' + esc(citation.articleTitle) + '"' : "";
    return '<tr class="' + (citation.selfCitation ? "row-self" : "") + '">' +
      '<td class="num"' + articleTip + ">" + esc(citation.id) + "</td>" +
      '<td class="num">' + esc(ids) + "</td>" +
      '<td class="num">' + esc(citation.year == null ? "—" : citation.year) + "</td>" +
      '<td class="cell-title">' + esc(citation.title || t("untitled")) + "</td>" +
      '<td class="cell-authors" title="' + esc((citation.authors || []).join("; ")) + '">' + authorsShort(citation.authors) + "</td>" +
      "<td>" + esc(citation.venue || "—") + "</td>" +
      '<td><span class="pill ' + typePill(citation.typeCode) + '">' + esc(typeLabel(citation.typeCode, citation.typeLabel)) + "</span></td>" +
      "<td>" + doi + "</td>" +
      '<td><span class="pill ' + (citation.selfCitation ? "pill-self" : "pill-neutral") + '">' + esc(citation.selfCitation ? t("yes") : t("no")) + "</span></td>" +
      "</tr>";
  }

  function chipSpec(kind) {
    if (kind === "pub") {
      var f = state.pubFilters;
      return [
        { key: "q", label: t("search"), value: f.q },
        { key: "author", label: t("author"), value: f.author },
        { key: "year", label: t("year"), value: f.year.join(", ") },
        { key: "type", label: t("type"), value: f.type.map(function (code) { return typeLabel(code); }).join(", ") },
        { key: "venue", label: t("venue"), value: f.venue.join(", ") },
        { key: "doiOnly", label: t("doiOnly"), value: f.doiOnly ? t("yes") : "" }
      ].filter(function (spec) { return spec.value; });
    }
    var c = state.citFilters;
    return [
      { key: "q", label: t("search"), value: c.q },
      { key: "author", label: t("author"), value: c.author },
      { key: "year", label: t("citYear"), value: c.year.join(", ") },
      { key: "article", label: t("article"), value: c.article.join(", ") },
      { key: "type", label: t("type"), value: c.type.map(function (code) { return typeLabel(code); }).join(", ") },
      { key: "venue", label: t("venue"), value: c.venue.join(", ") },
      { key: "doiOnly", label: t("doiOnly"), value: c.doiOnly ? t("yes") : "" },
      { key: "excludeSelf", label: t("excludeSelf"), value: c.excludeSelf ? t("yes") : "" }
    ].filter(function (spec) { return spec.value; });
  }

  function renderChips(kind) {
    var box = $(kind === "pub" ? "pubChips" : "citChips");
    box.innerHTML = chipSpec(kind).map(function (spec) {
      return '<span class="chip"><span>' + esc(spec.label) + ": " + esc(spec.value) + "</span>" +
        '<button type="button" data-chip="' + kind + ":" + spec.key + '" aria-label="' +
        esc(t("removeFilter")) + ": " + esc(spec.label) + '">×</button></span>';
    }).join("");
  }

  function onChipClick(event) {
    var btn = event.target && event.target.closest ? event.target.closest("[data-chip]") : null;
    if (!btn) return;
    var parts = btn.getAttribute("data-chip").split(":");
    var kind = parts[0], key = parts[1];
    if (kind === "pub") {
      state.pubFilters[key] = key === "doiOnly" ? false : [];
      state.pubPage = 1;
      syncControls(); renderPubTable(); renderPubCharts();
    } else {
      state.citFilters[key] = (key === "doiOnly" || key === "excludeSelf") ? false : [];
      state.citPage = 1;
      syncControls(); renderCitTable(); renderCitKpis(); renderCitCharts();
    }
    writeUrlState("push");
  }

  var CHARTS_KEY = "biblio-charts-collapsed";
  function setChartsCollapsed(kind, collapsed) {
    var row = $(kind === "pub" ? "pubChartsRow" : "citChartsRow");
    var btn = $(kind === "pub" ? "pubChartsToggle" : "citChartsToggle");
    row.hidden = collapsed;
    btn.setAttribute("aria-expanded", collapsed ? "false" : "true");
    var arrow = btn.querySelector(".charts-arrow");
    if (arrow) arrow.textContent = collapsed ? "›" : "▾";
    try { localStorage.setItem(CHARTS_KEY, collapsed ? "1" : "0"); } catch (error) { /* ignore */ }
    if (!collapsed) {
      Object.keys(state.charts).forEach(function (id) {
        var chart = state.charts[id];
        if (chart && chart.resize) chart.resize();
      });
    }
  }

  function applyChartsPref() {
    var collapsed;
    try {
      var saved = localStorage.getItem(CHARTS_KEY);
      collapsed = saved === "1" ? true : saved === "0" ? false : window.matchMedia("(max-width: 860px)").matches;
    } catch (error) {
      collapsed = false;
    }
    setChartsCollapsed("pub", collapsed);
    setChartsCollapsed("cit", collapsed);
  }

  function fillPageSelect(id, pages, current) {
    var select = $(id);
    select.innerHTML = "";
    for (var page = 1; page <= pages; page += 1) {
      var option = document.createElement("option");
      option.value = String(page);
      option.textContent = String(page);
      select.appendChild(option);
    }
    select.value = String(current);
  }

  function renderPubTable() {
    var rows = getFilteredPubs().sort(pubComparator());
    var total = rows.length;
    var pages = Math.max(1, Math.ceil(total / state.pubPageSize));
    state.pubPage = Math.min(Math.max(1, state.pubPage), pages);
    var start = (state.pubPage - 1) * state.pubPageSize;
    var pageRows = rows.slice(start, start + state.pubPageSize);
    var range = t("showingRange", {
      from: total ? start + 1 : 0,
      to: Math.min(start + state.pubPageSize, total),
      total: fmt(total)
    });

    $("pubTabCount").textContent = fmt(state.stats.publications);
    $("pubTableCount").textContent = total ? range : t("noResults");
    $("pubRange").textContent = range;
    fillPageSelect("pubPageSelect", pages, state.pubPage);
    $("pubFirst").disabled = state.pubPage <= 1;
    $("pubPrev").disabled = state.pubPage <= 1;
    $("pubNext").disabled = state.pubPage >= pages;
    $("pubLast").disabled = state.pubPage >= pages;
    $("pubBody").innerHTML = pageRows.length
      ? pageRows.map(pubRowHtml).join("")
      : '<tr class="empty-row"><td colspan="10">' + esc(t("noResults")) + "</td></tr>";
    $("emptyStatePub").hidden = total > 0;
    $("pubFilterResult").textContent = t("resultsFound", { total: fmt(total), all: fmt(state.pubs.length) });
    renderChips("pub");
    updateSortIndicators($("pubTable"), state.pubSort);
    Array.from(document.querySelectorAll("tr.pub-main")).forEach(function (row) {
      row.addEventListener("click", function () {
        var id = row.getAttribute("data-id");
        var detail = document.querySelector("tr.pub-detail[data-id=\"" + id + "\"]");
        if (detail) {
          var isHidden = detail.style.display === "none";
          detail.style.display = isHidden ? "" : "none";
          row.classList.toggle("pub-expanded", isHidden);
          row.setAttribute("aria-expanded", isHidden ? "true" : "false");
        }
      });
    });
  }

  function renderCitTable() {
    var rows = getFilteredCits().sort(citComparator());
    var total = rows.length;
    var pages = Math.max(1, Math.ceil(total / state.citPageSize));
    state.citPage = Math.min(Math.max(1, state.citPage), pages);
    var start = (state.citPage - 1) * state.citPageSize;
    var pageRows = rows.slice(start, start + state.citPageSize);
    var range = t("showingRange", {
      from: total ? start + 1 : 0,
      to: Math.min(start + state.citPageSize, total),
      total: fmt(total)
    });

    $("citTabCount").textContent = fmt(state.stats.works);
    $("citTableCount").textContent = total ? range : t("noResults");
    $("citRange").textContent = range;
    fillPageSelect("citPageSelect", pages, state.citPage);
    $("citFirst").disabled = state.citPage <= 1;
    $("citPrev").disabled = state.citPage <= 1;
    $("citNext").disabled = state.citPage >= pages;
    $("citLast").disabled = state.citPage >= pages;
    $("citBody").innerHTML = pageRows.length
      ? pageRows.map(citRowHtml).join("")
      : '<tr class="empty-row"><td colspan="9">' + esc(t("noResults")) + "</td></tr>";
    $("emptyStateCit").hidden = total > 0;
    $("citFilterResult").textContent = t("resultsFound", { total: fmt(total), all: fmt(state.cits.length) });
    renderChips("cit");
    updateSortIndicators($("citTable"), state.citSort);
  }

  function renderCitKpis() {
    var rows = getFilteredCits();
    var works = rows.length;
    var selfWorks = rows.filter(function (citation) { return citation.selfCitation; }).length;
    var links = rows.reduce(function (sum, citation) { return sum + citation._articleIds.length; }, 0);
    var selfLinks = rows.filter(function (citation) { return citation.selfCitation; }).reduce(function (sum, citation) {
      return sum + citation._articleIds.length;
    }, 0);
    var years = rows.map(function (citation) { return citation.year; }).filter(function (year) { return year != null; });
    var maxYear = years.length ? Math.max.apply(null, years) : null;
    var maxYearLinks = maxYear == null ? 0 : rows.filter(function (citation) {
      return citation.year === maxYear;
    }).reduce(function (sum, citation) { return sum + citation._articleIds.length; }, 0);

    $("citKpiWorks").textContent = fmt(works);
    $("citKpiExternal").textContent = t("kpiExternalSub", { n: fmt(works - selfWorks) });
    $("citKpiLinks").textContent = fmt(links);
    $("citKpiLinksSub").textContent = t("kpiLinksSub", { n: fmt(links - selfLinks) });
    $("citKpiSelf").textContent = fmt(selfWorks);
    $("citKpiMaxYear").textContent = maxYear == null ? "—" : String(maxYear);
    $("citKpiMaxYearSub").textContent = t("kpiMaxYearSub", { n: fmt(maxYearLinks) });
  }

  function cartesianOptions(horizontal) {
    return {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: horizontal ? "y" : "x",
      animation: { duration: 250 },
      plugins: {
        legend: { display: false },
        tooltip: { intersect: false, mode: "index" }
      },
      scales: horizontal ? {
        x: { beginAtZero: true, ticks: { precision: 0, font: { size: 10 }, color: "#64748b" }, grid: { color: "#edf1f6" } },
        y: { grid: { display: false }, ticks: { font: { size: 10 }, color: "#64748b" } }
      } : {
        x: { grid: { display: false }, ticks: { font: { size: 10 }, color: "#64748b" } },
        y: { beginAtZero: true, ticks: { precision: 0, font: { size: 10 }, color: "#64748b" }, grid: { color: "#edf1f6" } }
      }
    };
  }

  function doughnutOptions() {
    return {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 250 },
      plugins: {
        legend: { position: "bottom", labels: { boxWidth: 10, font: { size: 10 }, color: "#64748b" } }
      }
    };
  }

  function drawChart(id, config) {
    var canvas = $(id);
    if (!canvas || typeof Chart === "undefined") return;
    if (state.charts[id]) {
      state.charts[id].destroy();
      delete state.charts[id];
    }
    state.charts[id] = new Chart(canvas.getContext("2d"), config);
  }

  function hoverCursor(event, elements) {
    if (event && event.native && event.native.target) {
      event.native.target.style.cursor = elements && elements.length ? "pointer" : "default";
    }
  }

  function toggleValue(list, value) {
    var next = list.slice();
    var index = next.indexOf(value);
    if (index === -1) next.push(value); else next.splice(index, 1);
    return next;
  }

  function applyPubYearFilter(year) {
    var value = String(year);
    state.pubFilters.year = toggleValue(state.pubFilters.year, value);
    state.pubPage = 1;
    syncControls(); renderPubTable(); renderPubCharts();
    writeUrlState("push");
  }

  function applyPubTypeFilter(code) {
    var value = String(code);
    state.pubFilters.type = toggleValue(state.pubFilters.type, value);
    state.pubPage = 1;
    syncControls(); renderPubTable(); renderPubCharts();
    writeUrlState("push");
  }

  function applyCitYearFilter(year) {
    var value = String(year);
    state.citFilters.year = toggleValue(state.citFilters.year, value);
    state.citPage = 1;
    syncControls(); renderCitTable(); renderCitKpis(); renderCitCharts();
    writeUrlState("push");
  }

  function applyCitArticleFilter(articleId) {
    var value = String(articleId);
    state.citFilters.article = toggleValue(state.citFilters.article, value);
    state.citPage = 1;
    syncControls(); renderCitTable(); renderCitKpis(); renderCitCharts();
    writeUrlState("push");
  }

  function applyCitTypeFilter(code) {
    var value = String(code);
    state.citFilters.type = toggleValue(state.citFilters.type, value);
    var tab = $("tab-citari");
    if (tab) tab.checked = true;
    state.citPage = 1;
    syncControls(); renderCitTable(); renderCitKpis(); renderCitCharts();
    writeUrlState("push");
  }

  function renderPubCharts() {
    var rows = getFilteredPubs();
    var byYear = new Map();
    rows.forEach(function (pub) {
      if (pub.year != null) byYear.set(pub.year, (byYear.get(pub.year) || 0) + 1);
    });
    var years = Array.from(byYear.keys()).sort(function (a, b) { return a - b; });

    drawChart("pubYearChart", {
      type: "bar",
      data: {
        labels: years.map(String),
        datasets: [{
          label: t("tabPublications"),
          data: years.map(function (year) { return byYear.get(year); }),
          backgroundColor: "#2a7396",
          borderRadius: 4,
          maxBarThickness: 36
        }]
      },
      options: Object.assign(cartesianOptions(false), {
        onClick: function (event, elements) {
          if (elements && elements.length) applyPubYearFilter(years[elements[0].index]);
        },
        onHover: hoverCursor
      })
    });

    var byType = new Map();
    rows.forEach(function (pub) {
      byType.set(pub.typeCode, (byType.get(pub.typeCode) || 0) + 1);
    });
    var codes = Array.from(byType.keys());
    drawChart("pubTypeChart", {
      type: "doughnut",
      data: {
        labels: codes.map(function (code) { return typeLabel(code); }),
        datasets: [{
          data: codes.map(function (code) { return byType.get(code); }),
          backgroundColor: codes.map(function (code, index) { return PALETTE[index % PALETTE.length]; }),
          borderColor: "#ffffff",
          borderWidth: 1
        }]
      },
      options: Object.assign(doughnutOptions(), {
        onClick: function (event, elements) {
          if (elements && elements.length) applyPubTypeFilter(codes[elements[0].index]);
        },
        onHover: hoverCursor
      })
    });
  }

  function renderCitCharts() {
    var rows = getFilteredCits();
    var byYear = new Map();
    rows.forEach(function (citation) {
      if (citation.year != null) {
        byYear.set(citation.year, (byYear.get(citation.year) || 0) + citation._articleIds.length);
      }
    });
    var years = Array.from(byYear.keys()).sort(function (a, b) { return a - b; });

    drawChart("citYearChart", {
      type: "bar",
      data: {
        labels: years.map(String),
        datasets: [{
          label: t("kpiLinks"),
          data: years.map(function (year) { return byYear.get(year); }),
          backgroundColor: "#4c9fbf",
          borderRadius: 4,
          maxBarThickness: 36
        }]
      },
      options: Object.assign(cartesianOptions(false), {
        onClick: function (event, elements) {
          if (elements && elements.length) applyCitYearFilter(years[elements[0].index]);
        },
        onHover: hoverCursor
      })
    });

    var byArticle = new Map();
    rows.forEach(function (citation) {
      citation._articleIds.forEach(function (id) {
        byArticle.set(id, (byArticle.get(id) || 0) + 1);
      });
    });
    var titles = {};
    state.pubs.forEach(function (pub) { titles[pub.id] = pub.title; });
    var top = Array.from(byArticle.entries()).sort(function (a, b) {
      return b[1] - a[1] || a[0] - b[0];
    }).slice(0, 8);

    drawChart("citTopChart", {
      type: "bar",
      data: {
        labels: top.map(function (entry) {
          return "#" + entry[0] + " " + short(titles[entry[0]] || "", 24);
        }),
        datasets: [{
          label: t("kpiLinks"),
          data: top.map(function (entry) { return entry[1]; }),
          backgroundColor: "#2a7396",
          borderRadius: 3
        }]
      },
      options: Object.assign(cartesianOptions(true), {
        onClick: function (event, elements) {
          if (elements && elements.length) applyCitArticleFilter(top[elements[0].index][0]);
        },
        onHover: hoverCursor
      })
    });
  }

  function renderSynthesisCharts() {
    var byType = new Map();
    state.cits.forEach(function (citation) {
      byType.set(citation.typeCode, (byType.get(citation.typeCode) || 0) + 1);
    });
    var codes = Array.from(byType.keys());
    drawChart("citTypeChart", {
      type: "doughnut",
      data: {
        labels: codes.map(function (code) { return typeLabel(code); }),
        datasets: [{
          data: codes.map(function (code) { return byType.get(code); }),
          backgroundColor: codes.map(function (code, index) { return PALETTE[index % PALETTE.length]; }),
          borderColor: "#ffffff",
          borderWidth: 1
        }]
      },
      options: Object.assign(doughnutOptions(), {
        onClick: function (event, elements) {
          if (elements && elements.length) applyCitTypeFilter(codes[elements[0].index]);
        },
        onHover: hoverCursor
      })
    });
  }

  function renderMatrix() {
    var years = Array.from(new Set(state.cits.map(function (citation) { return citation.year; }).filter(function (year) {
      return year != null;
    }))).sort(function (a, b) { return a - b; });

    var rows = state.pubs.map(function (pub) {
      var cells = years.map(function (year) {
        return state.cits.reduce(function (sum, citation) {
          if (citation.year !== year) return sum;
          return sum + (citation._articleIds.indexOf(pub.id) !== -1 ? 1 : 0);
        }, 0);
      });
      return {
        id: pub.id,
        title: pub.title,
        cells: cells,
        total: cells.reduce(function (sum, value) { return sum + value; }, 0)
      };
    }).sort(function (a, b) {
      return b.total - a.total || a.id - b.id;
    });

    var totals = years.map(function (year, index) {
      return rows.reduce(function (sum, row) { return sum + row.cells[index]; }, 0);
    });
    var grand = totals.reduce(function (sum, value) { return sum + value; }, 0);

    $("matrixHead").innerHTML = '<tr><th class="num">' + esc(t("matrixArticle")) + "</th>" +
      years.map(function (year) { return '<th class="num">' + esc(year) + "</th>"; }).join("") +
      '<th class="num">' + esc(t("matrixTotal")) + "</th></tr>";

    var synSelect = $("synTitleFilter");
    var synPrev = synSelect.value;
    synSelect.innerHTML = '<option value="">' + esc(t("allArticles")) + "</option>" +
      rows.map(function (row) {
        return '<option value="' + esc(row.id) + '">#' + esc(row.id) + " · " + esc(short(row.title || "", 60)) + "</option>";
      }).join("");
    synSelect.value = synPrev || "";

    $("matrixBody").innerHTML = rows.map(function (row) {
      return '<tr data-id="' + esc(row.id) + '" data-title="' + esc(fold(row.title || "")) + '"><td class="num" title="' + esc(row.title) + '">' + esc(row.id) + "</td>" +
        row.cells.map(function (value) { return '<td class="num">' + fmt(value) + "</td>"; }).join("") +
        '<td class="num strong">' + fmt(row.total) + "</td></tr>";
    }).join("") +
      '<tr class="matrix-total"><td class="num">' + esc(t("matrixTotal")) + "</td>" +
      totals.map(function (value) { return '<td class="num">' + fmt(value) + "</td>"; }).join("") +
      '<td class="num strong">' + fmt(grand) + "</td></tr>";
  }

  function renderCoverage() {
    var pubs = state.pubs.slice().sort(function (a, b) {
      return b._citations - a._citations || a.id - b.id;
    });
    var top = pubs.filter(function (pub) { return pub._citations > 0; }).slice(0, 5);
    var zero = pubs.filter(function (pub) { return !pub._citations && pub.coverageStatus === "zero confirmat"; });
    var partial = pubs.filter(function (pub) { return !pub._citations && pub.coverageStatus === "parțial verificat - fără identificator"; });
    var max = top.length ? top[0]._citations : 1;
    var html = top.map(function (pub) {
      var width = Math.max(2, (pub._citations / max) * 100);
      return "<li><span>#" + esc(pub.id) + '</span><div class="track"><div class="fill" style="--w:' + width.toFixed(1) + '%"></div></div><b>' + fmt(pub._citations) + "</b></li>";
    }).join("");
    if (zero.length) {
      html += "<li><span>" + zero.map(function (pub) { return "#" + pub.id; }).join(", ") +
        '</span><div class="track"><div class="fill fill-empty" style="--w:100%"></div></div><b>0</b></li>';
    }
    $("coverageList").innerHTML = html;
    $("coverageBadge").textContent = t("coverageBadge", { n: fmt(zero.length) });
    if (partial.length) {
      $("partialCoverage").style.display = "";
      $("partialCoverageList").innerHTML = "<li><span>" + partial.map(function (pub) { return "#" + pub.id; }).join(", ") +
        '</span><div class="track"><div class="fill fill-partial" style="--w:100%"></div></div><b>' + t("coveragePartialBadge", { n: fmt(partial.length) }) + "</b></li>";
      $("partialCoverage").querySelector(".partial-title").textContent = t("coveragePartialBadge", { n: fmt(partial.length) });
    } else {
      $("partialCoverage").style.display = "none";
    }
  }

  function renderNotes() {
    var stats = state.stats;
    var items = [
      t("qa1", {
        links: fmt(stats.links),
        works: fmt(stats.works),
        self: fmt(stats.self),
        external: fmt(stats.works - stats.self)
      }),
      t("qa2"),
      t("qa3"),
      t("qa4")
    ];
    $("notesList").innerHTML = items.map(function (item) {
      return "<li>" + esc(item) + "</li>";
    }).join("");
  }

  function renderSynthesis() {
    var stats = state.stats;
    var articleCount = state.pubs.filter(function (pub) { return pub.typeCode === "article"; }).length;
    var externalLinks = stats.links - stats.selfLinks;

    $("synPubs").textContent = fmt(stats.publications);
    $("synPubsSub").textContent = t("synPubsSub", {
      articles: fmt(articleCount),
      other: fmt(stats.publications - articleCount)
    });
    $("synWorks").textContent = fmt(stats.works);
    $("synWorksSub").textContent = t("synWorksSub", { n: fmt(stats.works - stats.self) });
    $("synLinks").textContent = fmt(stats.links);
    $("synLinksSub").textContent = t("synLinksSub", { n: fmt(externalLinks) });
    $("synMissing").textContent = fmt(stats.missing);
    $("synMissingSub").textContent = t("synMissingSub", { n: fmt(stats.publications) });

    renderMatrix();
    renderCoverage();
    renderNotes();
  }

  function repoFileUrl(path) {
    if (!path) return "";
    var clean = String(path).replace(/^\.\.\//, "").replace(/^\//, "");
    return "https://raw.githubusercontent.com/narcis101993/bibliographic-dashboard/main/" + clean;
  }

  function setDownload(id, csvPath) {
    var el = $(id);
    if (!el) return;
    if (csvPath) {
      el.href = repoFileUrl(String(csvPath).replace(/\.csv$/i, ".xlsx"));
      el.hidden = false;
    } else {
      el.hidden = true;
    }
  }

  function sourceLabel(info) {
    if (!info || !info.centralizator || !info.centralizator.csv) return "—";
    return info.centralizator.csv.replace(/^\.\.\//, "").replace(/\.csv$/i, ".xlsx");
  }

  function renderSources() {
    var sources = (state.manifest && state.manifest.sources) || [];
    $("sourcesList").innerHTML = sources.map(function (source) {
      var count;
      if (source.count == null) {
        count = t("sourceNoCount");
      } else if (source.countKind === "manualImport") {
        count = t("sourceLinks", { n: fmt(source.count) }) + " · " + t("sourceManual");
      } else if (source.countKind === "citationLinks") {
        count = t("sourceLinks", { n: fmt(source.count) });
      } else {
        count = t("sourcePubs", { n: fmt(source.count) });
      }
      return '<li><span class="source-dot source-ok"></span><div><b>' + esc(source.name) + "</b><span>" + esc(count) +
        '</span></div><a href="' + esc(source.url) + '" target="_blank" rel="noopener" aria-label="' + esc(source.name) + '">↗</a></li>';
    }).join("");
  }

  function renderMeta() {
    var manifest = state.manifest || {};
    var info = (manifest.versions || []).filter(function (item) {
      return item.version === state.version;
    })[0];

    $("metaExtracted").textContent = formatDate(manifest.dataExtractedAt);
    $("metaPubs").textContent = fmt(state.stats.publications);
    $("metaWorks").textContent = fmt(state.stats.works);
    $("versionChip").textContent = state.version || "—";
    $("updatedLabel").textContent = t("updated") + " " + formatDate(manifest.dataExtractedAt);

    var extracted = (manifest.dataExtractedAt || "").slice(0, 10);
    var now = new Date();
    var today = now.getFullYear() + "-" + String(now.getMonth() + 1).padStart(2, "0") + "-" + String(now.getDate()).padStart(2, "0");
    var isFresh = extracted !== "" && extracted === today;
    var pill = $("freshPill");
    pill.className = "pill " + (isFresh ? "pill-ok" : "pill-warn");
    pill.textContent = t(isFresh ? "pillCurrent" : "pillStale");

    setDownload("downloadXlsx", info && info.centralizator && info.centralizator.csv);
    setDownload("downloadCitXlsx", info && info.citari && info.citari.csv);
    setDownload("downloadSynXlsx", state.version ? "citari/" + state.version + "/Acoperire_Publicatii_v4.xlsx" : "");

    renderSources();
  }

  function renderDetect() {
    // Detection status used to live in a banner; it was removed.
    // Kept as a no-op so renderAll() stays unchanged.
  }

  function renderPanelSubtitles() {
    $("pubPanelSub").textContent = t("pubPanelSub", {
      n: fmt(state.stats.publications),
      articles: fmt(state.pubs.filter(function (pub) { return pub.typeCode === "article"; }).length),
      doi: fmt(state.pubs.filter(function (pub) { return !!pub.doi; }).length)
    });
    $("citPanelSub").textContent = t("citPanelSub", {
      n: fmt(state.stats.works),
      links: fmt(state.stats.links),
      self: fmt(state.stats.self)
    });
  }

  function renderAll() {
    applyI18n();
    populateFilters();
    syncControls();
    renderPanelSubtitles();
    renderDetect();
    renderMeta();
    renderPubTable();
    renderPubCharts();
    renderCitTable();
    renderCitKpis();
    renderCitCharts();
    renderSynthesis();
    renderSynthesisCharts();
  }

  function onPubFilterChange() {
    state.pubFilters.q = $("pubSearch").value;
    state.pubFilters.author = $("pubAuthor").value;
    state.pubFilters.year = selectedValues($("pubYear"));
    state.pubFilters.type = selectedValues($("pubType"));
    state.pubFilters.venue = selectedValues($("pubVenue"));
    state.pubFilters.doiOnly = $("pubDoiOnly").checked;
    state.pubPage = 1;
    renderPubTable();
    renderPubCharts();
    writeUrlState("replace");
  }

  function onCitFilterChange() {
    state.citFilters.q = $("citSearch").value;
    state.citFilters.author = $("citAuthor").value;
    state.citFilters.year = selectedValues($("citYear"));
    state.citFilters.article = selectedValues($("citArticle"));
    state.citFilters.venue = selectedValues($("citVenue"));
    state.citFilters.type = selectedValues($("citType"));
    state.citFilters.doiOnly = $("citDoiOnly").checked;
    state.citFilters.excludeSelf = $("citExcludeSelf").checked;
    state.citPage = 1;
    renderCitTable();
    renderCitKpis();
    renderCitCharts();
    writeUrlState("replace");
  }

  function resetPubFilters() {
    state.pubFilters = { q: "", author: "", year: [], type: [], venue: [], doiOnly: false };
    state.pubPage = 1;
    syncControls();
    renderPubTable();
    renderPubCharts();
    writeUrlState("push");
  }

  function resetCitFilters() {
    state.citFilters = { q: "", author: "", year: [], article: [], type: [], venue: [], doiOnly: false, excludeSelf: false };
    state.citPage = 1;
    syncControls();
    renderCitTable();
    renderCitKpis();
    renderCitCharts();
    writeUrlState("push");
  }

  function toggleSort(sort, key) {
    if (sort.key === key) {
      sort.dir = sort.dir === "asc" ? "desc" : "asc";
    } else {
      sort.key = key;
      sort.dir = (key === "id" || key === "year" || key === "citations" || key === "articleId" || key === "self") ? "desc" : "asc";
    }
  }

  function csvCell(value) {
    var text = String(value == null ? "" : value);
    if (/[;"\r\n]/.test(text)) {
      return '"' + text.replace(/"/g, '""') + '"';
    }
    return text;
  }

  function exportCsv(filename, headers, rows) {
    var lines = [headers.map(csvCell).join(";")];
    rows.forEach(function (row) {
      lines.push(row.map(csvCell).join(";"));
    });
    var blob = new Blob(["\uFEFF" + lines.join("\r\n")], { type: "text/csv;charset=utf-8" });
    var url = URL.createObjectURL(blob);
    var link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  function exportPublications() {
    var rows = getFilteredPubs().sort(pubComparator());
    exportCsv(
      "publications_" + (state.version || "data") + "_filtered.csv",
      [t("colNr"), t("colYear"), t("colTitle"), t("colVenue"), t("colType"), t("colDoi"), t("colCitations"), t("colAuthors")],
      rows.map(function (pub) {
        return [pub.id, pub.year, pub.title, pub.venue, typeLabel(pub.typeCode, pub.typeLabel), pub.doi, pub._citations || 0, (pub.authors || []).join("; ")];
      })
    );
  }

  function exportCitations() {
    var rows = getFilteredCits().sort(citComparator());
    exportCsv(
      "citations_" + (state.version || "data") + "_filtered.csv",
      [t("colNr"), t("colArticle"), t("colCitYear"), t("colCiting"), t("colAuthors"), t("colVenue"), t("colType"), t("colDoi"), t("colSelf"), t("sourceFile")],
      rows.map(function (citation) {
        return [citation.id, citation._articleIds.join(", "), citation.year, citation.title, (citation.authors || []).join("; "), citation.venue, typeLabel(citation.typeCode, citation.typeLabel), citation.doi, citation.selfCitation ? t("yes") : t("no"), citation.source];
      })
    );
  }

  function showToast(message) {
    var old = document.querySelector(".app-toast");
    if (old) old.remove();
    var toast = document.createElement("div");
    toast.className = "app-toast";
    toast.setAttribute("role", "status");
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(function () {
      if (toast.parentNode) toast.remove();
    }, 15000);
  }

  function redetect() {
    var button = $("redetect");
    var label = button.querySelector("[data-i18n]");
    var prevVersion = state.version;
    var prevExtract = state.manifest && state.manifest.dataExtractedAt;
    var prevDigest = state.manifest && state.manifest.inputDigest;
    button.disabled = true;
    if (label) label.textContent = t("rescanning");
    loadData().then(function () {
      renderAll();
      var updated = state.version !== prevVersion ||
        (state.manifest && (state.manifest.dataExtractedAt !== prevExtract || state.manifest.inputDigest !== prevDigest));
      showToast(t(updated ? "toastUpdated" : "toastFresh"));
    }).catch(function (error) {
      showLoadError(error);
    }).finally(function () {
      button.disabled = false;
      if (label) label.textContent = t("redetect");
    });
  }

  function showLoadError(error) {
    console.error("[dashboard]", error);
    var existing = document.querySelector(".app-status.is-error");
    if (existing) existing.remove();
    var notice = document.createElement("div");
    notice.className = "app-status is-error";
    notice.textContent = t("loadError") + " " + (error && error.message ? error.message : "");
    var workspace = document.querySelector(".workspace");
    if (workspace) workspace.parentNode.insertBefore(notice, workspace);
  }

  function bindEvents() {
    $("pubSearch").addEventListener("input", onPubFilterChange);
    $("pubAuthor").addEventListener("input", onPubFilterChange);
    bindMulti("pubYear", onPubFilterChange);
    bindMulti("pubType", onPubFilterChange);
    bindMulti("pubVenue", onPubFilterChange);
    document.addEventListener("click", closeAllMulti);
    document.addEventListener("scroll", function (event) {
      if (event.target && event.target.closest && event.target.closest(".multi-panel")) return;
      closeAllMulti();
    }, true);
    window.addEventListener("resize", closeAllMulti);
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closeAllMulti();
    });
    $("pubDoiOnly").addEventListener("change", onPubFilterChange);
    $("pubReset").addEventListener("click", resetPubFilters);
    $("emptyResetPub").addEventListener("click", resetPubFilters);
    $("pubCopyLink").addEventListener("click", function () { copyCurrentLink("pubCopyMsg"); });
    $("pubChips").addEventListener("click", onChipClick);
    $("pubPageSize").addEventListener("click", function (event) {
      var button = event.target.closest ? event.target.closest("button[data-size]") : null;
      if (!button) return;
      state.pubPageSize = parseInt(button.getAttribute("data-size"), 10) || PUB_PAGE_SIZE;
      state.pubPage = 1;
      setPageSizeButtons("pubPageSize", state.pubPageSize);
      renderPubTable();
    });
    $("synFilterReset").addEventListener("click", function () {
      $("synTitleFilter").value = "";
      document.querySelectorAll("#matrixBody tr[data-id]").forEach(function (row) {
        row.style.display = "";
      });
    });
    $("synTitleFilter").addEventListener("change", function () {
      var selected = $("synTitleFilter").value;
      document.querySelectorAll("#matrixBody tr[data-id]").forEach(function (row) {
        row.style.display = !selected || row.getAttribute("data-id") === selected ? "" : "none";
      });
    });
    $("pubChartsToggle").addEventListener("click", function () {
      setChartsCollapsed("pub", !$("pubChartsRow").hidden);
    });

    $("citSearch").addEventListener("input", onCitFilterChange);
    $("citAuthor").addEventListener("input", onCitFilterChange);
    bindMulti("citYear", onCitFilterChange);
    bindMulti("citArticle", onCitFilterChange);
    bindMulti("citVenue", onCitFilterChange);
    bindMulti("citType", onCitFilterChange);
    $("citDoiOnly").addEventListener("change", onCitFilterChange);
    $("citExcludeSelf").addEventListener("change", onCitFilterChange);
    $("citReset").addEventListener("click", resetCitFilters);
    $("emptyResetCit").addEventListener("click", resetCitFilters);
    $("citCopyLink").addEventListener("click", function () { copyCurrentLink("citCopyMsg"); });
    $("citChips").addEventListener("click", onChipClick);
    $("citPageSize").addEventListener("click", function (event) {
      var button = event.target.closest ? event.target.closest("button[data-size]") : null;
      if (!button) return;
      state.citPageSize = parseInt(button.getAttribute("data-size"), 10) || CIT_PAGE_SIZE;
      state.citPage = 1;
      setPageSizeButtons("citPageSize", state.citPageSize);
      renderCitTable();
    });
    $("citChartsToggle").addEventListener("click", function () {
      setChartsCollapsed("cit", !$("citChartsRow").hidden);
    });

    document.querySelectorAll("#pubTable th[data-sort]").forEach(function (header) {
      header.setAttribute("tabindex", "0");
      header.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          header.click();
        }
      });
      header.addEventListener("click", function () {
        toggleSort(state.pubSort, header.getAttribute("data-sort"));
        renderPubTable();
        writeUrlState("push");
      });
    });
    document.querySelectorAll("#citTable th[data-sort]").forEach(function (header) {
      header.setAttribute("tabindex", "0");
      header.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          header.click();
        }
      });
      header.addEventListener("click", function () {
        toggleSort(state.citSort, header.getAttribute("data-sort"));
        renderCitTable();
        writeUrlState("push");
      });
    });

    $("pubFirst").addEventListener("click", function () {
      if (state.pubPage !== 1) {
        state.pubPage = 1;
        renderPubTable();
        writeUrlState("push");
      }
    });
    $("pubLast").addEventListener("click", function () {
      var pages = Math.max(1, Math.ceil(getFilteredPubs().length / state.pubPageSize));
      if (state.pubPage !== pages) {
        state.pubPage = pages;
        renderPubTable();
        writeUrlState("push");
      }
    });
    $("pubPageSelect").addEventListener("change", function () {
      state.pubPage = parseInt($("pubPageSelect").value, 10) || 1;
      renderPubTable();
      writeUrlState("push");
    });
    $("pubPrev").addEventListener("click", function () {
      if (state.pubPage > 1) {
        state.pubPage -= 1;
        renderPubTable();
        writeUrlState("push");
      }
    });
    $("pubNext").addEventListener("click", function () {
      state.pubPage += 1;
      renderPubTable();
      writeUrlState("push");
    });
    $("citFirst").addEventListener("click", function () {
      if (state.citPage !== 1) {
        state.citPage = 1;
        renderCitTable();
        writeUrlState("push");
      }
    });
    $("citLast").addEventListener("click", function () {
      var pages = Math.max(1, Math.ceil(getFilteredCits().length / state.citPageSize));
      if (state.citPage !== pages) {
        state.citPage = pages;
        renderCitTable();
        writeUrlState("push");
      }
    });
    $("citPageSelect").addEventListener("change", function () {
      state.citPage = parseInt($("citPageSelect").value, 10) || 1;
      renderCitTable();
      writeUrlState("push");
    });
    $("citPrev").addEventListener("click", function () {
      if (state.citPage > 1) {
        state.citPage -= 1;
        renderCitTable();
        writeUrlState("push");
      }
    });
    $("citNext").addEventListener("click", function () {
      state.citPage += 1;
      renderCitTable();
      writeUrlState("push");
    });

    document.querySelectorAll(".tab-input").forEach(function (input) {
      input.addEventListener("change", function () {
        if (input.checked) writeUrlState("push");
      });
    });

    $("redetect").addEventListener("click", redetect);
    $("refreshData").addEventListener("click", function () {
      var url = new URL(window.location.href);
      url.searchParams.set("_t", Date.now());
      window.location.href = url.toString();
    });

    document.querySelectorAll(".lang-btn").forEach(function (button) {
      button.addEventListener("click", function () {
        var lang = button.getAttribute("data-lang");
        if (lang === state.lang) return;
        state.lang = lang;
        try { localStorage.setItem(LANG_KEY, lang); } catch (error) { /* storage may be blocked on file:// */ }
        renderAll();
        writeUrlState("push");
      });
    });

    document.querySelectorAll(".theme-btn").forEach(function (button) {
      button.addEventListener("click", function () {
        var theme = button.getAttribute("data-theme-value");
        if ((theme === "dark") === state.dark) return;
        state.dark = theme === "dark";
        try { localStorage.setItem(DARK_KEY, state.dark ? "1" : "0"); } catch (error) { /* ignore */ }
        applyTheme();
        applyI18n();
      });
    });

    window.addEventListener("popstate", onUrlPopState);
  }

  function registerServiceWorker() {
    // Service workers need a secure context (https or localhost) and a
    // real origin — skip silently on file:// and other unsupported setups.
    if (!("serviceWorker" in navigator)) return;
    if (!/^https?:$/.test(window.location.protocol)) return;
    navigator.serviceWorker.register("sw.js").catch(function () { /* optional */ });
  }

  function init() {
    var urlState = readUrlState();
    registerServiceWorker();

    try {
      var saved = localStorage.getItem(LANG_KEY);
      if (saved === "ro" || saved === "en") state.lang = saved;
    } catch (error) { /* ignore */ }

    try {
      var darkSaved = localStorage.getItem(DARK_KEY);
      state.dark = darkSaved === "1";
    } catch (error) { /* ignore */ }

    if (urlState.lang === "ro" || urlState.lang === "en") state.lang = urlState.lang;

    bindEvents();
    applyI18n();
    applyTheme();
    applyChartsPref();
    showLoading();
    loadData().then(function () {
      hideLoading();
      applyUrlState(urlState);
      writeUrlState("replace");
      try { localStorage.setItem(LANG_KEY, state.lang); } catch (error) { /* storage may be blocked on file:// */ }
      try { localStorage.setItem(DARK_KEY, state.dark ? "1" : "0"); } catch (error) { /* ignore */ }
      renderAll();
    }).catch(function(error) {
      hideLoading();
      showLoadError(error);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
