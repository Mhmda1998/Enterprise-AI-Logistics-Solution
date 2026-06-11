<div align="center">

# 🚚 Enterprise AI Logistics Solution

### The Future of Autonomous Supply Chain Intelligence

**Developed by Mohammed Ibrahim Ghabban** *(GEAR Certified Developer)* 🇾🇪

<p align="center">
  <a href="https://github.com/Mhmda1998/Enterprise-AI-Logistics-Solution/stargazers"><img src="https://img.shields.io/github/stars/Mhmda1998/Enterprise-AI-Logistics-Solution?style=for-the-badge&logo=star&logoColor=white" alt="Stars"/></a>
  <a href="https://github.com/Mhmda1998/Enterprise-AI-Logistics-Solution/network/members"><img src="https://img.shields.io/github/forks/Mhmda1998/Enterprise-AI-Logistics-Solution?style=for-the-badge&logo=git&logoColor=white" alt="Forks"/></a>
  <a href="https://github.com/Mhmda1998/Enterprise-AI-Logistics-Solution/issues"><img src="https://img.shields.io/github/issues/Mhmda1998/Enterprise-AI-Logistics-Solution?style=for-the-badge&logo=github&logoColor=white" alt="Issues"/></a>
  <a href="https://github.com/Mhmda1998/Enterprise-AI-Logistics-Solution/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Mhmda1998/Enterprise-AI-Logistics-Solution?style=for-the-badge" alt="License"/></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/GEAR_Certified-Developer-FFD700?style=for-the-badge&logo=target&logoColor=white" alt="GEAR Certified"/>
  <img src="https://img.shields.io/badge/AI_Specialist-Gemini_Pro-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="AI Specialist"/>
  <img src="https://img.shields.io/badge/Cloud_Architecture-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker DevOps"/>
</p>

</div>

---

## 📋 Overview | نظرة عامة

An **Enterprise-grade Autonomous Logistics Agent** powered by **Google Gemini 1.5 Pro**. This system transforms complex supply chain data into actionable intelligence, optimizing routes and reducing costs for global enterprises.

نظام ذكاء اصطناعي لوجستي عالمي مستقل (Autonomous Agent) يعمل بتقنية **Google Gemini 1.5 Pro**. يحول بيانات سلاسل التوريد المعقدة إلى رؤى قابلة للتنفيذ، ويحسّن المسارات ويقلل التكاليف للمؤسسات العالمية.

---

## ✨ Key Features | الميزات الرئيسية

- 🧠 **Smart AI Agent:** Advanced logistics analysis powered by Gemini 1.5 Pro
- 📊 **Interactive Dashboard:** Real-time analytics and visualization (Streamlit)
- 📈 **Smart Visualizations:** Beautiful charts and graphs (Plotly & Pandas)
- 🛠️ **Secure & Scalable:** Containerized with Docker for production deployment
- 🔐 **API Authentication:** Secure API key-based access control
- 📝 **Full Documentation:** Comprehensive docs, examples, and API reference
- ✅ **Fully Tested:** 100% test coverage with pytest
- 🚀 **CI/CD Ready:** GitHub Actions pipeline included
- 🌍 **Production-Ready:** Enterprise-grade error handling and logging

---

## 🏗️ Architecture | البنية المعمارية

```
┌─────────────────────────────────────────┐
│           Streamlit Dashboard           │
│         (Real-time Analytics)           │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│          FastAPI Backend                │
│  • Health checks  • Auth & validation   │
│  • Pydantic models • CORS support       │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│      Google Gemini 1.5 Pro             │
│   (AI Analysis Engine)                  │
└─────────────────────────────────────────┘
```

---

## 🚀 Quick Start | بدء سريع

### Option 1: Docker (Recommended)

Run the entire enterprise system with ONE command:

```bash
docker-compose up --build
```

This will start:
- 🌐 API on `http://localhost:8000`
- 📊 Dashboard on `http://localhost:8501`

### Option 2: Local Development

```bash
# 1. Clone the repository
git clone https://github.com/Mhmda1998/Enterprise-AI-Logistics-Solution.git
cd Enterprise-AI-Logistics-Solution

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 5. Run the API
uvicorn src.api:app --reload

# 6. In another terminal, run the dashboard
streamlit run src/dashboard.py
```

---

## 📚 Documentation | التوثيق

- 📘 [API Reference](docs/API.md) — Complete API documentation
- 🏛️ [Architecture Guide](docs/ARCHITECTURE.md) — System design & modules
- 🤝 [Contributing Guide](CONTRIBUTING.md) — How to contribute
- 💖 [Support Guide](SUPPORT.md) — How to support the project
- 🏆 [Sponsors](SPONSOR.md) — Sponsor tiers and benefits
- 💡 [Usage Examples](examples/) — Code examples and sample data

---

## 🎯 Usage Examples | أمثلة الاستخدام

### Using cURL

```bash
curl -X POST "http://localhost:8000/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Optimize delivery routes for 500 packages across 3 cities",
    "context": "Route,Distance,Cost\nR1,120km,$450",
    "api_key": "YOUR_GEMINI_API_KEY"
  }'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/analyze",
    json={
        "prompt": "Optimize delivery routes for 500 packages across 3 cities",
        "api_key": "YOUR_GEMINI_API_KEY"
    }
)
print(response.json()["ai_response"])
```

More examples in [`examples/`](examples/) directory.

---

## 🛠️ Tech Stack | التقنيات المستخدمة

| Layer | Technology |
|-------|------------|
| **Language** | Python 3.10+ |
| **API Framework** | FastAPI |
| **UI Framework** | Streamlit |
| **AI Model** | Google Gemini 1.5 Pro |
| **Validation** | Pydantic v2 |
| **Containerization** | Docker, Docker Compose |
| **Testing** | pytest |
| **CI/CD** | GitHub Actions |
| **Linting** | Ruff |
| **Charts** | Plotly, Pandas |

---

## 🧪 Testing | الاختبارات

Run the full test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_api.py
```

---

## 🐳 Docker Deployment | النشر بـ Docker

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 📂 Project Structure | هيكل المشروع

```
Enterprise-AI-Logistics-Solution/
├── src/
│   ├── __init__.py
│   ├── api.py            # FastAPI application
│   ├── dashboard.py      # Streamlit dashboard
│   ├── services.py       # AI business logic
│   ├── models.py         # Pydantic schemas
│   ├── config.py         # Settings management
│   └── utils.py          # Utility functions
├── tests/
│   ├── test_api.py       # API tests
│   ├── test_models.py    # Model tests
│   └── test_utils.py     # Utility tests
├── docs/
│   ├── API.md            # API documentation
│   └── ARCHITECTURE.md   # Architecture guide
├── examples/
│   ├── api_client.py     # Python client example
│   └── sample_data.json  # Sample logistics data
├── .github/
│   └── workflows/
│       └── ci.yml        # CI/CD pipeline
├── Dockerfile            # Backend container
├── Dockerfile.ui         # Dashboard container
├── docker-compose.yml    # Multi-container orchestration
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore
├── LICENSE
├── README.md
├── CONTRIBUTING.md
├── SUPPORT.md
├── SPONSOR.md
└── CHANGELOG.md
```

---

## 🛡️ Security | الأمان

- ✅ API key authentication (per-request or env-based)
- ✅ CORS configuration
- ✅ Input validation via Pydantic
- ✅ Secrets excluded via `.gitignore`
- ✅ Automated dependency scanning via GitHub Actions
- ✅ Container security via Docker isolation

---

## 🗺️ Roadmap | خارطة الطريق

- [x] Core AI engine with Gemini 1.5 Pro
- [x] Streamlit dashboard
- [x] Docker containerization
- [x] Comprehensive test suite
- [x] CI/CD pipeline
- [x] API documentation
- [x] Sponsorship & support channels
- [ ] WebSocket support for real-time updates
- [ ] Multi-tenant support
- [ ] Integration with ERP systems (SAP, Oracle)
- [ ] Mobile app (React Native)
- [ ] Advanced analytics with ML predictions
- [ ] Multi-language support (Arabic, English, French)

---

## 🤝 Contributing | المساهمة

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License | الرخصة

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.

---

## 👤 Author | المؤلف

**Mohammed Ibrahim Ghabban** *(GEAR Certified AI Developer)*

- 🌐 GitHub: [@Mhmda1998](https://github.com/Mhmda1998)
- 📧 Email: 734402368n@gmail.com
- 📍 Location: Sana'a, Yemen 🇾🇪
- 🎓 Certifications: Google GEAR, AI Specialist, Docker DevOps

---

## 🙏 Acknowledgments | شكر وتقدير

- Google Gemini team for the powerful AI model
- The open-source community for amazing tools
- All contributors and users of this project

---

## 💖 Show your Support | أظهر دعمك

If this project helped you, please support it! See [SUPPORT.md](SUPPORT.md) for all the ways you can help.

<p align="center">
  <a href="https://github.com/Mhmda1998/Enterprise-AI-Logistics-Solution"><img src="https://img.shields.io/badge/⭐_Star_this_Repo-black?style=for-the-badge" alt="Star"/></a>
  &nbsp;
  <a href="https://github.com/Mhmda1998/Enterprise-AI-Logistics-Solution/issues"><img src="https://img.shields.io/badge/🐛_Report_Bug-black?style=for-the-badge" alt="Report Bug"/></a>
  &nbsp;
  <a href="https://github.com/Mhmda1998/Enterprise-AI-Logistics-Solution/blob/main/SUPPORT.md"><img src="https://img.shields.io/badge/💖_Sponsor-black?style=for-the-badge" alt="Sponsor"/></a>
</p>

---

<div align="center">

**Built with ❤️ by Mohammed Ghabban • GEAR Certified Developer**

</div>
