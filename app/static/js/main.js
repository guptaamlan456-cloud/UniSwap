document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.classList.remove('show');
      alert.classList.add('hide');
    }, 6000);
  });

  const nancyToggle = document.getElementById('nancy-toggle');
  const nancyPanel = document.getElementById('nancy-panel');
  const nancyClose = document.getElementById('nancy-close');
  const nancyActions = document.getElementById('nancy-actions');
  const nancyBody = document.getElementById('nancy-body');

  if (!nancyToggle || !nancyPanel || !nancyActions || !nancyBody) return;

  const addNancyMessage = (text) => {
    const message = document.createElement('div');
    message.className = 'nancy-message';
    message.textContent = text;
    nancyBody.appendChild(message);
  };

  const resetNancyActions = () => {
    nancyActions.innerHTML = '';

    const sellBtn = document.createElement('button');
    sellBtn.type = 'button';
    sellBtn.className = 'btn btn-primary btn-sm';
    sellBtn.textContent = 'Sell';
    sellBtn.dataset.nancyAction = 'sell';

    const buyBtn = document.createElement('button');
    buyBtn.type = 'button';
    buyBtn.className = 'btn btn-outline-primary btn-sm';
    buyBtn.textContent = 'Buy';
    buyBtn.dataset.nancyAction = 'buy';

    nancyActions.appendChild(sellBtn);
    nancyActions.appendChild(buyBtn);
  };

  nancyToggle.addEventListener('click', () => {
    nancyPanel.classList.toggle('d-none');
  });

  if (nancyClose) {
    nancyClose.addEventListener('click', () => {
      nancyPanel.classList.add('d-none');
    });
  }

  nancyActions.addEventListener('click', async (event) => {
    const button = event.target.closest('button[data-nancy-action]');
    if (!button) return;
    const action = button.dataset.nancyAction;

    if (action === 'sell') {
      window.location.href = '/listings/create';
      return;
    }

    if (action === 'buy') {
      addNancyMessage('What do you want to buy?');
      nancyActions.innerHTML = '';

      const input = document.createElement('input');
      input.type = 'text';
      input.className = 'form-control form-control-sm';
      input.placeholder = 'Type product name';

      const findBtn = document.createElement('button');
      findBtn.type = 'button';
      findBtn.className = 'btn btn-primary btn-sm';
      findBtn.textContent = 'Find';

      nancyActions.appendChild(input);
      nancyActions.appendChild(findBtn);

      findBtn.addEventListener('click', async () => {
        const query = (input.value || '').trim();
        if (!query) {
          addNancyMessage('Please type a product name first.');
          return;
        }

        try {
          const response = await fetch(`/nancy/search?q=${encodeURIComponent(query)}`);
          const result = await response.json();
          addNancyMessage(result.message);
          if (result.found && result.url) {
            window.location.href = result.url;
            return;
          }
        } catch (_) {
          addNancyMessage('Sorry, something went wrong while searching.');
        }

        resetNancyActions();
      });
    }
  });
});
