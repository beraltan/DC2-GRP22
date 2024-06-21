import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, kstest, norm, probplot

# Histogram and Q-Q plot for Average Score
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
sns.histplot(data['Average Score'], kde=True, ax=ax[0])
ax[0].set_title('Histogram of Average Score')
probplot(data['Average Score'], dist="norm", plot=ax[1])
ax[1].set_title('Q-Q Plot of Average Score')

# Normality test for Average Score
shapiro_test = shapiro(data['Average Score'])
kstest_test = kstest(data['Average Score'], 'norm', args=(data['Average Score'].mean(), data['Average Score'].std()))

plt.show()

print(f"Shapiro-Wilk test: Statistic={shapiro_test.statistic}, p-value={shapiro_test.pvalue}")
print(f"Kolmogorov-Smirnov test: Statistic={kstest_test.statistic}, p-value={kstest_test.pvalue}")
