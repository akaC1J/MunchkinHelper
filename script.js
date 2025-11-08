const searchBox = document.getElementById('searchBox');
const filterBtns = document.querySelectorAll('.filter-btn');
const sections = document.querySelectorAll('.section');
const noResults = document.getElementById('noResults');

let currentSection = 'all';

// Обработка переключения фильтров
filterBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        filterBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        currentSection = this.dataset.section;
        applyFilters();
    });
});

// Обработка поиска
searchBox.addEventListener('input', applyFilters);

function applyFilters() {
    const term = searchBox.value.toLowerCase().trim();
    let visibleCount = 0;
    const shownIds = new Set(); // отслеживаем уже показанные rule-id

    sections.forEach(section => {
        const sectionName = section.dataset.section;
        const isCardSection = sectionName.startsWith('Карта:');
        const matchesFilter = (currentSection === 'all') ||
                              (sectionName === currentSection);
        let sectionVisible = false;

        section.querySelectorAll('.rule-card').forEach(card => {
            const id = card.dataset.ruleId;
            const text = card.textContent.toLowerCase();
            const match = text.includes(term);

            // показываем только первое вхождение id
            const visible = ((matchesFilter && !isCardSection) || isCardSection)
                            && (term === '' || match)
                            && !shownIds.has(id);

            card.classList.toggle('hidden', !visible);
            if (visible) {
                shownIds.add(id);
                sectionVisible = true;
                visibleCount++;
            }
        });

        section.style.display = sectionVisible ? 'block' : 'none';
    });

    noResults.style.display = visibleCount === 0 ? 'block' : 'none';
}
