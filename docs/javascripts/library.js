/* Progressive enhancement: keep tables intact inside keyboard-scrollable regions. */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.rw-book-image').forEach(image => {
    const showPlaceholder = () => { image.hidden = true; };
    image.addEventListener('error', showPlaceholder);
    if (image.complete && image.naturalWidth === 0) showPlaceholder();
  });
  document.querySelectorAll('[role="main"] table').forEach((table, index) => {
    if (table.parentElement.classList.contains('rw-table-scroll')) return;
    const wrapper = document.createElement('div');
    wrapper.className = 'rw-table-scroll';
    wrapper.tabIndex = 0;
    wrapper.setAttribute('role', 'region');
    wrapper.setAttribute('aria-label', table.caption?.textContent.trim() || `Reference table ${index + 1}`);
    table.before(wrapper);
    wrapper.appendChild(table);
  });
});
