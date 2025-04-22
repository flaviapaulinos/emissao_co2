import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set_theme(palette="bright")

PALETTE = "coolwarm"
SCATTER_ALPHA = 0.2

def grafico_componentes(estudo_pca):
    fig, ax = plt.subplots()
    
    ax.plot(
        range(1, estudo_pca['pca'].n_components_ +1),#a contagem de componentes normalmente começa com 1
        np.cumsum(estudo_pca['pca'].explained_variance_ratio_),
        color='C1',
       
    )
    ax.axhline(y=0.85, color="C5", linestyle='--', label='85% Variância')
    
    ax.axhline(y=0.95, color="C4", linestyle='--', label='95% Variância')
    ax.axhline(y=0.98, color="C0", linestyle='--', label='98% Variância')
    
    
    ax.bar(
        x=range(1, estudo_pca['pca'].n_components_ +1),
        height= estudo_pca['pca'].explained_variance_ratio_,
        color='C0',
        alpha=0.5
    )
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    ax.grid(linestyle=':')
    
    ax.set_xlabel("Número de componentes")
    ax.set_ylabel("Variância Explicada")
    ax.set_title("Scree plot")
    
    ax.legend()
        
    plt.show()


def plot_coeficientes(df_coefs, titulo="Coeficientes"):
    df_coefs.plot.barh(figsize=(9,12))
    plt.title(titulo)
    plt.axvline(x=0, color=".5")
    plt.xlabel("Coeficientes")
    plt.gca().get_legend().remove()
    plt.tight_layout()
    plt.show()



def plot_comparar_metricas_modelos(df_resultados, multi_class=False):
    fig, axs = plt.subplots(4, 2, figsize=(9, 9), sharex=True)

    comparar_metricas = [
        "time_seconds",
        "test_accuracy",
        "test_balanced_accuracy",
        "test_f1" if not multi_class else "test_f1_weighted",
        "test_precision" if not multi_class else "test_precision_weighted",
        "test_recall" if not multi_class else "test_recall_weighted",
        "test_roc_auc" if not multi_class else "test_roc_auc_ovr",
        "test_average_precision",
        #"test_f2_score"
    ]

    nomes_metricas = [
        "Tempo (s)",
        "Acurácia",
        "Acurácia balanceada",
        "F1",
        "Precisão",
        "Recall",
        "AUROC",
        "AUPRC",
        #"F2"
    ]

    for ax, metrica, nome in zip(axs.flatten(), comparar_metricas, nomes_metricas):
        sns.boxplot(
            x="model",
            y=metrica,
            data=df_resultados,
            ax=ax,
            showmeans=True,
        )
        ax.set_title(nome)
        ax.set_ylabel(nome)
        ax.tick_params(axis="x", rotation=90)

    plt.tight_layout()

    plt.show()