import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import json

if __name__ == "__main__":
    cur_dir = Path(__file__).parent
    data_path = cur_dir / "data" / "econ_data.csv"
    df = pd.read_csv(data_path)
    print(df.head())
    print(df.columns)

    col_list = df.columns.tolist()
    start_idx = df.columns.get_loc("village_committees_count")
    target_cols = col_list[start_idx + 1 :]
    target_numeric_cols = df[target_cols].select_dtypes(include=[np.number]).columns.tolist()
    print(target_numeric_cols)
    df_target = df[target_numeric_cols]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_target)
    pca = PCA(n_components=7)
    pca_features = pca.fit_transform(X_scaled)

    print(f"Original number of features: {X_scaled.shape[1]}")
    print(f"Reduced number of features after PCA: {pca_features.shape[1]}")
    print("Explained variance ratio of each principal component:")
    for i, ratio in enumerate(pca.explained_variance_ratio_):
        print(f"PC{i + 1}: {ratio:.4f}")

    plt.figure(figsize=(10, 5))
    plt.plot(range(1, len(pca.explained_variance_ratio_) + 1), 
         np.cumsum(pca.explained_variance_ratio_), marker='o', linestyle='--')
    plt.title('Cumulative Explained Variance')
    plt.xlabel('Number of Components')
    plt.ylabel('Cumulative Explained Variance')
    plt.axhline(y=0.50, color='r', linestyle='-') # 50% threshold line
    plt.grid()
    plt.savefig('pca_variance_plot_4.png', dpi=300, bbox_inches='tight')
    plt.show()

    loadings = pd.DataFrame(
        pca.components_.T,
        columns=[f'PC{i+1}' for i in range(7)],
        index=target_numeric_cols
    )
    print("PCA Loadings:")
    print(loadings)

    plt.figure(figsize=(20, 12))
    sns.heatmap(loadings, annot=True, cmap='coolwarm', center=0)
    plt.title('PCA Loadings Heatmap')
    plt.savefig('pca_loadings_heatmap_1.png', dpi=300, bbox_inches='tight')
    plt.show()
    pca_features_df = pd.DataFrame(
        pca_features,
        columns=[f'PC{i+1}' for i in range(pca_features.shape[1])]
    )
    print("PCA Transformed Features:")
    print(pca_features_df.head())
    pca_features_df.to_csv(cur_dir / "data" / "econ_data_pca.csv", index=False)
    print("PCA transformed data saved to 'econ_data_pca.csv'")
    
    plt.figure(figsize=(10, 5))
    plt.bar(range(1, len(pca.explained_variance_ratio_) + 1), pca.explained_variance_ratio_)
    plt.title('Explained Variance by Each Principal Component')
    plt.xlabel('Principal Component')
    plt.ylabel('Explained Variance Ratio')
    plt.grid()
    plt.savefig('pca_variance_plot_4.png', dpi=300, bbox_inches='tight')
    plt.show()

    top_variables_list = {}
    for i in range(1, 8):
        col_name = f'PC{i}'
        top_10 = loadings[col_name].abs().sort_values(ascending=False).head(10).index.tolist()
        top_variables_list[col_name] = top_10
    print("Top 10 contributing variables for each principal component:")
    for pc, variables in top_variables_list.items():
        print(f"{pc}: {variables}")

    with open(cur_dir / "data" / "pca_top_variables.json", "w") as f:
        json.dump(top_variables_list, f, indent=4)

    pca_cols = [
        "Demographic_Scale",
        "General_Economic_Dev",
        "Agri_and_Mechanization",
        "Public_Service_Energy",
        "Industrial_Fiscal_Perf",
        "Institution_Cultural",
        "Advanced_Urban_Quality"
    ]
    df_pca_scores = pd.DataFrame(pca_features, columns=pca_cols, index=df.index)
    df_final = pd.concat([df[['year', 'province', 'city', 'admin_code']], df_pca_scores], axis=1)
    df_final.to_csv("county_characteristics_pca.csv", index=False)
    