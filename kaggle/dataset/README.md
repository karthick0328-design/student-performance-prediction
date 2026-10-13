# Dataset Documentation: Student Performance Dataset

## 1. Source and Attribution
- **Dataset Name:** Student Performance Data Set
- **Source:** UC Irvine Machine Learning Repository (UCI ML)
- **Creators:** Paulo Cortez and Alice Silva (University of Minho, Guimarães, Portugal)
- **Original Publication:** 
  Cortez, P., & Silva, A. (2008). *Using Data Mining to Predict Secondary School Student Performance*. In Proceedings of 5th Annual Future Business Technology Conference (FUBUTEC 2008), pp. 5-12, Porto, Portugal.
- **License / Terms:** Creative Commons Attribution 4.0 International (CC BY 4.0). Available freely for public research and education.

## 2. Dataset Files
- `student-mat.csv`: Student achievement in secondary education of Math course (395 instances, 33 attributes).
- `student-por.csv`: Student achievement in Portuguese language course (649 instances, 33 attributes).
- `student.txt`: Original attribute metadata and descriptions.

## 3. Features Breakdown (30 Predictors + 3 Period Grades)

### Demographic and Family
1. `school`: Student's school ('GP' - Gabriel Pereira or 'MS' - Mousinho da Silveira)
2. `sex`: Student's sex ('F' - female or 'M' - male)
3. `age`: Student's age (numeric: 15 to 22)
4. `address`: Home address type ('U' - urban or 'R' - rural)
5. `famsize`: Family size ('LE3' - <= 3 or 'GT3' - > 3)
6. `Pstatus`: Parent's cohabitation status ('T' - living together or 'A' - apart)
7. `Medu`: Mother's education (0 - none, 1 - 4th grade, 2 - 5th-9th grade, 3 - secondary, 4 - higher)
8. `Fedu`: Father's education (0 - none, 1 - 4th grade, 2 - 5th-9th grade, 3 - secondary, 4 - higher)
9. `Mjob`: Mother's job ('teacher', 'health', 'services', 'at_home', 'other')
10. `Fjob`: Father's job ('teacher', 'health', 'services', 'at_home', 'other')
11. `reason`: Reason to choose school ('home', 'reputation', 'course', 'other')
12. `guardian`: Student's guardian ('mother', 'father', 'other')

### Academic Context and Support
13. `traveltime`: Home to school travel time (1: <15 min, 2: 15-30 min, 3: 30-60 min, 4: >60 min)
14. `studytime`: Weekly study time (1: <2 hrs, 2: 2-5 hrs, 3: 5-10 hrs, 4: >10 hrs)
15. `failures`: Past class failures (numeric: 0, 1, 2, 3)
16. `schoolsup`: Extra educational support ('yes' or 'no')
17. `famsup`: Family educational support ('yes' or 'no')
18. `paid`: Extra paid classes within subject ('yes' or 'no')
19. `activities`: Extra-curricular activities ('yes' or 'no')
20. `nursery`: Attended nursery school ('yes' or 'no')
21. `higher`: Wants to take higher education ('yes' or 'no')
22. `internet`: Internet access at home ('yes' or 'no')
23. `romantic`: With a romantic relationship ('yes' or 'no')

### Lifestyle and Social
24. `famrel`: Quality of family relationships (1 - very bad to 5 - excellent)
25. `freetime`: Free time after school (1 - very low to 5 - very high)
26. `goout`: Going out with friends (1 - very low to 5 - very high)
27. `Dalc`: Workday alcohol consumption (1 - very low to 5 - very high)
28. `Walc`: Weekend alcohol consumption (1 - very low to 5 - very high)
29. `health`: Current health status (1 - very bad to 5 - very good)
30. `absences`: Number of school absences (numeric: 0 to 93)

### Target and Excluded Features
- `G1`: First period grade (0 - 20) — **Excluded from model input** to prevent target leakage and enable true early intervention.
- `G2`: Second period grade (0 - 20) — **Excluded from model input** to prevent target leakage.
- `G3`: **Final grade (0 - 20) — Target Variable**.
