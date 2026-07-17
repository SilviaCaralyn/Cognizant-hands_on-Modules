# SeleniumBasics — Digital Nurture 5.0 (organised by Hands-On)

```
YourName/
├── HandsOn1/  qa_concepts.md
├── HandsOn2/  v_model_analysis.md
├── HandsOn3/  automation_strategy.md
├── HandsOn4/  setup_test.py, navigation_test.py
├── HandsOn5/  setup_test.py (helper), locators_test.py, waits_test.py
├── HandsOn6/  conftest.py, test_playground.py
├── HandsOn7/  conftest.py, pages/, tests/test_pom_suite.py
└── requirements.txt
```

Each folder is self-contained and runnable on its own.

## One-time setup

```bash
mv HandsOnStructured/YourName HandsOnStructured/<YourActualName>
cd HandsOnStructured/<YourActualName>

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Chrome must be installed. `webdriver-manager` auto-downloads the matching ChromeDriver.

## Running each Hands-On

```bash
# Hands-On 4
cd HandsOn4
python setup_test.py
python navigation_test.py
cd ..

# Hands-On 5
cd HandsOn5
python locators_test.py
python waits_test.py
cd ..

# Hands-On 6
cd HandsOn6
pytest test_playground.py -v --html=report.html --self-contained-html
cd ..

# Hands-On 7
cd HandsOn7
pytest tests/ -v --html=report.html --self-contained-html
cd ..
```

## Verify zero find_element calls in the POM test file (Hands-On 7, step 59)

```bash
grep -rn "find_element" HandsOn7/tests/
# Should return nothing
```

## Push to GitHub

```bash
git init
git add .
git commit -m "Digital Nurture 5.0 - Selenium Basics hands-on submission"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```
