const animalService = {
    async listAnimals(apiKey, filters = {}, page = 1) {
        const queryParams = new URLSearchParams({
            offset: (page - 1) * 20,
            limit: 20,
            ...Object.fromEntries(
                Object.entries(filters).filter(([_, v]) => v !== '')
            )
        });

        const response = await fetch(`/api/animals?${queryParams}`, {
            headers: {
                'X-API-Key': apiKey,
            }
        });
        if (!response.ok) throw new Error('Failed to fetch animals');
        return response.json();
    },

    async addAnimal(animalData, apiKey) {
        const response = await fetch('/api/animals', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': apiKey,
            },
            body: JSON.stringify(animalData),
        });
        if (!response.ok) throw new Error('Failed to add animal');
        return response.json();
    },

    async deleteAnimal(animalId, apiKey) {
        const response = await fetch(`/api/animals/${animalId}`, {
            method: 'DELETE',
            headers: {
                'X-API-Key': apiKey,
            },
        });
        if (!response.ok) throw new Error('Failed to delete animal');
    },

    async importAnimals(file, apiKey) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/shelter/import-animals', {
            method: 'POST',
            headers: {
                'X-API-Key': apiKey,
            },
            body: formData,
        });
        if (!response.ok) throw new Error('Failed to import animals');
    },

    async generateDescription(animalId, apiKey) {
        const response = await fetch(`/api/animals/${animalId}/generate-description`, {
            method: 'POST',
            headers: {
                'X-API-Key': apiKey,
            },
        });
        if (!response.ok) throw new Error('Failed to generate description');
        return response.json();
    }
};

export default animalService;