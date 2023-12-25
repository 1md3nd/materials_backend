# Material API
### The Material API provides endpoints for managing materials. It allows users to retrieve information about materials, search for specific materials, and more.
---
### You can access the APIs at http://34.125.107.238:8080/ 
## NOTE: use only HTTP to make requests HTTPS will not work.


## Endpoints
### Get All Materials
#### Endpoint:
```
GET /get_all_materials/
```
### Description:
This endpoint retrieves information about all materials stored in the database.

#### Responses:
- 200 OK:
```
{
    "0": {
        "_id": "65886531724ba2cee80b4262",
        "Unnamed: 0": 0,
        "nsites": 44,
        "formula_pretty": "Ti19N25",
        "volume": 487.2834764308068,
        "density": 4.292536811308379,
        "symmetry__crystal_system": "Trigonal",
        "symmetry__symbol": "R-3m",
        "symmetry__number": 166,
        "symmetry__point_group": "-3m",
        "symmetry__symprec": 0.1,
        "symmetry__version": "2.0.2",
        "formation_energy_per_atom": -1.309148
    }
}
```
- 500 Internal Server Error:

    - An error occurred on the server.

### Search Materials
#### Endpoint:
```
GET /search_materials/
```

#### Parameters:
- element: Search by a single element.
- elements: Search by multiple elements (comma-separated).
- containsonly: Search by materials containing only specified elements (comma-separated).
- sort_field: Sort fields (comma-separated).
- sort_order: Sort order (asc/desc) for each sort field (comma-separated).

#### Description:
This endpoint allows users to search for materials based on various criteria.

#### Responses:
- 200 OK:
```
{
    "status": "197 data found.",
    "data": {
        "0": {
            "_id": "6588d787b1960e838230e4e0",
            "Unnamed: 0": 55,
            "nsites": 6,
            "formula_pretty": "Ti",
            "volume": 208.54801594917905,
            "density": 2.2868121704973263,
            "symmetry__crystal_system": "Trigonal",
            "symmetry__symbol": "P-3m1",
            "symmetry__number": 164,
            "symmetry__point_group": "-3m",
            "symmetry__symprec": 0.1,
            "symmetry__version": "2.0.2",
            "formation_energy_per_atom": 0.3103078066666664,
            "energy_above_hull": 0.3103078066666658,
            "is_stable": false,
            "band_gap": 0.0,
            "is_gap_direct": false,
            "is_metal": true,
            "ordering": "FM",
            "total_magnetization": 1.609971,
            "universal_anisotropy": "",
            "theoretical": true,
            "compounds_contain": "Ti",
            "compounds_contain_count": 1
        },
    }
}
```

- 500 Internal Server Error:

    - An error occurred on the server.
---
## How to Run Locally

### 1. Clone the repository:
```bash
git clone https://github.com/1md3nd/materials_backend.git
```

### 2. Install dependencies:

```bash
cd materials_backend
pip install -r requirements.txt
```
### 3.Run the server:
```bash
python manage.py runserver
```
The application will be accessible at http://localhost:8000

---

## Running with Docker
### 1. Build the Docker image:
```bash
docker build -t material-server .
```

### 2. Run the Docker container:

```bash
docker run -p 8080:8080 material-server
```
The application will be accessible at http://localhost:8000.

---

 #### Feel free to reach me out anurag.botmaster@outlook.com

