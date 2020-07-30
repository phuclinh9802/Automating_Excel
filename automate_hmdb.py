from splinter import Browser
from selenium import webdriver
import time
import requests


# open chrome browser and visit website

def browser_open(website_path):
    # add chrome driver to execute
    # To use this, you need to download chromedriver from https://chromedriver.chromium.org/downloads and choose
    # the version of google chrome you are using. Then, specify the path in executable variable like below.
    executable = {'executable_path': r'/Users/phucnguyen/Desktop/chromedriver'}

    options = webdriver.ChromeOptions()

    options.add_argument("--window-size=1400,900")
    options.add_argument("--start-maximized")

    options.add_argument("--disable-notification")

    browser = Browser('chrome', **executable, headless=False, options=options)

    browser.visit(website_path)

    return browser

# visit hmdb.ca to automate
def automate_hmdb(table, adduct, tolerance_number):
    # open hmdb.ca website
    browser = browser_open("https://hmdb.ca/spectra/ms/search")

    # find id for textarea - query_masses
    # query_mass = browser.find_by_id("query_masses")

    browser.fill("query_masses", '\n'.join(str(t - 1) for t in table))

    adduct_type = browser.find_by_id("adduct_type")
    for a in adduct:
        adduct_type.select(a)

    browser.fill("tolerance", tolerance_number)

    tolerance = browser.find_by_id("tolerance_units")
    tolerance.select("ppm")

    # submit button -- search
    submit = browser.find_by_name("commit").first.click()
    # time.sleep(3)
    # download as csv
    submit_1 = browser.find_by_value("Download Results As CSV").first.click()

def removing(string):
    return "".join(string.split("  "))

def automate_kegg(kegg_list):
    # open map pathway website
    browser = browser_open("https://www.genome.jp/kegg/tool/map_pathway1.html")
    # rno mode
    rno = browser.find_by_id("s_map")
    rno.fill("rno")

    textarea = browser.find_by_id("s_q")
    textarea.fill('\n'.join(str(k) for k in kegg_list))

    browser.find_by_value("Exec").first.click()

    browser.click_link_by_text('Show matched objects')
    print(browser.find_by_css("ul pre li:nth-child(2) a:nth-child(1)").value)
    a = 1
    count = 0
    try:
        while browser.find_by_css("ul pre li:nth-child(" + str(a) + ") a:nth-child(1)").value is not None:
            count += 1
            a += 1
    except:
        print("Loop is done")
    list = browser.find_by_css("ul pre li:nth-child(2) div").value.split("\n")
    # print(list)

    for x in range(len(list)):
        list[x] = removing(list[x])
        # print(list[x])
    # print(browser.find_by_css("ul pre li:nth-child(1) div a:nth-child(1)").value)


    i = 1
    j = 1
    path_i = 0
    kegg = []
    pathway = get_pathways("http://rest.kegg.jp/list/pathway/rno")
    path_len = len(pathway[0])
    print(path_len)
    pathway_arr = []
    metabolism_arr = []

    # print(browser.find_by_css("ul pre li:nth-child(" + str(j) + ") div a:nth-child(" + str(i) + ")").value)
    # print(browser.find_by_css("ul pre li:nth-child(" + str(j) + ") a:nth-child(1)").value)

    pw_list = []
    while j <= count:
        if browser.find_by_css("ul pre li:nth-child(" + str(j) + ") a:nth-child(1)").value in pathway[0]:
            ind = pathway[0].index(browser.find_by_css("ul pre li:nth-child(" + str(j) + ") a:nth-child(1)").value)
            pw_list.append(pathway[1][ind])
            j += 1

    print(pw_list)

    # try:
    #     for d in dict:
    #         if browser.find_by_css("ul pre li:nth-child(" + str(j) + ") div a:nth-child(" + str(i) + ")").value in d:
    #             while browser.find_by_css("ul pre li:nth-child(" + str(j) + ") a:nth-child(1)").valu

    # try:
    #     # while j <= count:
    #     #     while browser.find_by_css("ul pre li:nth-child(" + str(j) + ") div a:nth-child(" + str(i) + ")").value is not None and path_i < path_len:
    #     #         for x in range(path_len):
    #     #             if browser.find_by_css("ul pre li:nth-child(" + str(j) + ") a:nth-child(1)").value == pathway[0][path_i]:
    #     #                 pathway_arr.append(pathway[0][path_i])
    #     #             else:
    #     #                 path_i += 1
    #     #         kegg.append(browser.find_by_css("ul pre li:nth-child("+ str(j) + ") div a:nth-child(" + str(i) + ")").value)
    #     #         i += 1
    #     #     j += 1
    #
    #
    # except:
    #     print("Loop has been stopped!")


    # print(kegg)
    time.sleep(86400)

# get pathways - metabolism data
def get_pathways(rest):
    response = requests.get(rest)
    content = response.content
    decoded_string = content.decode("unicode_escape")

    list = decoded_string.split(" - Rattus norvegicus (rat)\n")
    for x in range(len(list)):
        list[x] = list[x].split("\t")
        # print(list[x])

    for x in range(len(list)):
        list[x][0] = list[x][0][5:13]

    # remove last element
    list.pop()

    transpose = []

    for x in range(len(list[0])):
        record = []
        for y in range(len(list)):
            record.append(list[y][x])
        transpose.append(record)


    print(transpose)

    return transpose

# get_pathways("http://rest.kegg.jp/list/pathway/rno")


dict = [{ 'Metabolic pathways': 'Global and overview maps' },
        { 'Biosynthesis of secondary metabolites': 'Global and overview maps' },
        { 'Microbial metabolism in diverse environments': 'Global and overview maps' },
        { 'Carbon metabolism': 'Global and overview maps' },
        { '2-Oxocarboxylic acid metabolism': 'Global and overview maps' },
        { 'Fatty acid metabolism': 'Global and overview maps' },
        { 'Biosynthesis of amino acids': 'Global and overview maps' },
        { 'Degradation of aromatic compounds': 'Global and overview maps' },
        { 'Glycolysis / Gluconeogenesis': 'Carbohydrate metabolism'},
        { 'Citrate cycle (TCA cycle)': 'Carbohydrate metabolism'},
        { 'Pentose phosphate pathway': 'Carbohydrate metabolism'},
        { 'Pentose and glucuronate interconversions': 'Carbohydrate metabolism'},
        { 'Fructose and mannose metabolism': 'Carbohydrate metabolism'},
        { 'Galactose metabolism': 'Carbohydrate metabolism'},
        { 'Ascorbate and aldarate metabolism': 'Carbohydrate metabolism'},
        { 'Starch and sucrose metabolism': 'Carbohydrate metabolism'},
        { 'Amino sugar and nucleotide sugar metabolism': 'Carbohydrate metabolism'},
        { 'Pyruvate metabolism': 'Carbohydrate metabolism'},
        { 'Glyoxylate and dicarboxylate metabolism': 'Carbohydrate metabolism'},
        { 'Propanoate metabolism': 'Carbohydrate metabolism'},
        { 'Butanoate metabolism': 'Carbohydrate metabolism'},
        { 'C5-Branched dibasic acid metabolism': 'Carbohydrate metabolism'},
        { 'Inositol phosphate metabolism': 'Carbohydrate metabolism'},
        { 'Oxidative phosphorylation': 'Energy metabolism'},
        { 'Photosynthesis': 'Energy metabolism'},
        { 'Photosynthesis - antenna proteins': 'Energy metabolism'},
        { 'Carbon fixation in photosynthetic organisms': 'Energy metabolismm'},
        { 'Carbon fixation pathways in prokaryotes': 'Energy metabolism'},
        { 'Methane metabolism': 'Energy metabolism'},
        { 'Nitrogen metabolism': 'Energy metabolism'},
        { 'Sulfur metabolism': 'Energy metabolism'},
        { 'Fatty acid biosynthesis': 'Lipid metabolism'},
        { 'Fatty acid elongation': 'Lipid metabolism'},
        { 'Fatty acid degradation': 'Lipid metabolism'},
        { 'Synthesis and degradation of ketone bodies': 'Lipid metabolism'},
        { 'Cutin, suberine and wax biosynthesis': 'Lipid metabolism'},
        { 'Steroid biosynthesis': 'Lipid metabolism'},
        { 'Primary bile acid biosynthesis': 'Lipid metabolism'},
        { 'Secondary bile acid biosynthesis': 'Lipid metabolism'},
        { 'Steroid hormone biosynthesis': 'Lipid metabolism'},
        { 'Glycerolipid metabolism': 'Lipid metabolism'},
        { 'Glycerophospholipid metabolism': 'Lipid metabolism'},
        { 'Ether lipid metabolism': 'Lipid metabolism'},
        { 'Sphingolipid metabolism': 'Lipid metabolism'},
        { 'Arachidonic acid metabolism': 'Lipid metabolism'},
        { 'Linoleic acid metabolism': 'Lipid metabolism'},
        { 'alpha-Linolenic acid metabolism': 'Lipid metabolism'},
        { 'Biosynthesis of unsaturated fatty acids': 'Lipid metabolism'},
        { 'Purine metabolism': 'Nucleotide metabolism'},
        { 'Pyrimidine metabolism': 'Nucleotide metabolism'},
        { 'Alanine, aspartate and glutamate metabolism': 'Amino acid metabolism'},
        { 'Glycine, serine and threonine metabolism': 'Amino acid metabolism'},
        { 'Cysteine and methionine metabolism': 'Amino acid metabolism'},
        { 'Valine, leucine and isoleucine degradation': 'Amino acid metabolism'},
        { 'Valine, leucine and isoleucine biosynthesis': 'Amino acid metabolism'},
        { 'Lysine biosynthesis': 'Amino acid metabolism'},
        { 'Lysine degradation': 'Amino acid metabolism'},
        { 'Arginine biosynthesis': 'Amino acid metabolism'},
        { 'Arginine and proline metabolism': 'Amino acid metabolism'},
        { 'Histidine metabolism': 'Amino acid metabolism'},
        { 'Tyrosine metabolism': 'Amino acid metabolism'},
        { 'Phenylalanine metabolism': 'Amino acid metabolism'},
        { 'Tryptophan metabolism': 'Amino acid metabolism'},
        { 'Phenylalanine, tyrosine and tryptophan biosynthesis': 'Amino acid metabolism'},
        { 'beta-Alanine metabolism': 'Metabolism of other amino acids'},
        { 'Taurine and hypotaurine metabolism': 'Metabolism of other amino acids'},
        { 'Phosphonate and phosphinate metabolism': 'Metabolism of other amino acids'},
        { 'Selenocompound metabolism': 'Metabolism of other amino acids'},
        { 'Cyanoamino acid metabolism': 'Metabolism of other amino acids'},
        { 'D-Glutamine and D-glutamate metabolism': 'Metabolism of other amino acids'},
        { 'D-Arginine and D-ornithine metabolism': 'Metabolism of other amino acids'},
        { 'D-Alanine metabolism': 'Metabolism of other amino acids'},
        { 'Glutathione metabolism': 'Metabolism of other amino acids'},
        { 'N-Glycan biosynthesis': 'Glycan biosynthesis and metabolism'},
        { 'Various types of N-glycan biosynthesis': 'Glycan biosynthesis and metabolism'},
        { 'Mucin type O-glycan biosynthesis': 'Glycan biosynthesis and metabolism'},
        { 'Mannose type O-glycan biosynthesis': 'Glycan biosynthesis and metabolism'},
        { 'Other types of O-glycan biosynthesis': 'Glycan biosynthesis and metabolism'},
        { 'Glycosaminoglycan biosynthesis - chondroitin sulfate / dermatan sulfate': 'Glycan biosynthesis and metabolism'},
        { 'Glycosaminoglycan biosynthesis - heparan sulfate / heparin': 'Glycan biosynthesis and metabolism'},
        { 'Glycosaminoglycan biosynthesis - keratan sulfate': 'Glycan biosynthesis and metabolism'},
        { 'Glycosaminoglycan degradation': 'Glycan biosynthesis and metabolism'},
        { 'Glycosylphosphatidylinositol (GPI)-anchor biosynthesis': 'Glycan biosynthesis and metabolism'},
        { 'Glycosphingolipid biosynthesis - lacto and neolacto series': 'Glycan biosynthesis and metabolism'},
        { 'Glycosphingolipid biosynthesis - globo and isoglobo series': 'Glycan biosynthesis and metabolism'},
        { 'Glycosphingolipid biosynthesis - ganglio series': 'Glycan biosynthesis and metabolism'},
        { 'Lipopolysaccharide biosynthesis': 'Glycan biosynthesis and metabolism'},
        { 'Peptidoglycan biosynthesis': 'Glycan biosynthesis and metabolism'},
        { 'Other glycan degradation': 'Glycan biosynthesis and metabolism'},
        { 'Lipoarabinomannan (LAM) biosynthesis': 'Glycan biosynthesis and metabolism'},
        { 'Arabinogalactan biosynthesis - Mycobacterium': 'Glycan biosynthesis and metabolism'},
        { 'Thiamine metabolism': 'Metabolism of cofactors and vitamins'},
        { 'Riboflavin metabolism': 'Metabolism of cofactors and vitamins'},
        { 'Vitamin B6 metabolism': 'Metabolism of cofactors and vitamins'},
        { 'Nicotinate and nicotinamide metabolism': 'Metabolism of cofactors and vitamins'},
        { 'Pantothenate and CoA biosynthesis': 'Metabolism of cofactors and vitamins'},
        { 'Biotin metabolism': 'Metabolism of cofactors and vitamins'},
        { 'Lipoic acid metabolism': 'Metabolism of cofactors and vitamins'},
        { 'Folate biosynthesis': 'Metabolism of cofactors and vitamins'},
        { 'One carbon pool by folate': 'Metabolism of cofactors and vitamins'},
        { 'Retinol metabolism': 'Metabolism of cofactors and vitamins'},
        { 'Porphyrin and chlorophyll metabolism': 'Metabolism of cofactors and vitamins'},
        { 'Ubiquinone and other terpenoid-quinone biosynthesis': 'Metabolism of cofactors and vitamins'},
        { 'Terpenoid backbone biosynthesis': 'Metabolism of terpenoids and polyketides'},
        { 'Monoterpenoid biosynthesis': 'Metabolism of terpenoids and polyketides'},
        { 'Sesquiterpenoid and triterpenoid biosynthesis': 'Metabolism of terpenoids and polyketides'},
        { 'Diterpenoid biosynthesis': 'Metabolism of terpenoids and polyketides'},
        { 'Carotenoid biosynthesis': 'Metabolism of terpenoids and polyketides'},
        { 'Brassinosteroid biosynthesis': 'Metabolism of terpenoids and polyketides'},
        { 'Insect hormone biosynthesis': 'Metabolism of terpenoids and polyketides'},
        { 'Zeatin biosynthesis': 'Metabolism of terpenoids and polyketides'},
        { 'Limonene and pinene degradation': 'Metabolism of terpenoids and polyketides'},
        { 'Geraniol degradation': 'Metabolism of terpenoids and polyketides'},
        { 'Type I polyketide structures': 'Metabolism of terpenoids and polyketides'},
        { 'Biosynthesis of 12-, 14- and 16-membered macrolides': 'Metabolism of terpenoids and polyketides'},
        { 'Biosynthesis of ansamycins': 'Metabolism of terpenoids and polyketides'},
        { 'Biosynthesis of enediyne antibiotics': 'Metabolism of terpenoids and polyketides'},
        { 'Biosynthesis of type II polyketide backbone': 'Metabolism of terpenoids and polyketides'},
        { 'Biosynthesis of type II polyketide products': 'Metabolism of terpenoids and polyketides'},
        { 'Tetracycline biosynthesis': 'Metabolism of terpenoids and polyketides'},
        { 'Polyketide sugar unit biosynthesis': 'Metabolism of terpenoids and polyketides'},
        { 'Nonribosomal peptide structures': 'Metabolism of terpenoids and polyketides'},
        { 'Biosynthesis of siderophore group nonribosomal peptides': 'Metabolism of terpenoids and polyketides'},
        { 'Biosynthesis of vancomycin group antibiotics': 'Metabolism of terpenoids and polyketides'},
        { 'Phenylpropanoid biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Stilbenoid, diarylheptanoid and gingerol biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Flavonoid biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Flavone and flavonol biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Anthocyanin biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Isoflavonoid biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Indole alkaloid biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Indole diterpene alkaloid biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Isoquinoline alkaloid biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Tropane, piperidine and pyridine alkaloid biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Acridone alkaloid biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Caffeine metabolism': 'Biosynthesis of other secondary metabolites'},
        { 'Betalain biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Glucosinolate biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Benzoxazinoid biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Penicillin and cephalosporin biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Carbapenem biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Monobactam biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Clavulanic acid biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Streptomycin biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Neomycin, kanamycin and gentamicin biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Acarbose and validamycin biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Novobiocin biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Staurosporine biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Phenazine biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Prodigiosin biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Aflatoxin biosynthesis': 'Biosynthesis of other secondary metabolites'},
        { 'Biosynthesis of various secondary metabolites - part 1': 'Biosynthesis of other secondary metabolites'},
        { 'Biosynthesis of various secondary metabolites - part 2': 'Biosynthesis of other secondary metabolites'},
        { 'Biosynthesis of various secondary metabolites - part 3': 'Biosynthesis of other secondary metabolites'},
        { 'Benzoate degradation': 'Xenobiotics biodegradation and metabolism'},
        { 'Aminobenzoate degradation': 'Xenobiotics biodegradation and metabolism'},
        { 'Fluorobenzoate degradation': 'Xenobiotics biodegradation and metabolism'},
        { 'Chloroalkane and chloroalkene degradation': 'Xenobiotics biodegradation and metabolism'},
        { 'Chlorocyclohexane and chlorobenzene degradation': 'Xenobiotics biodegradation and metabolism'},
        { 'Toluene degradation': 'Xenobiotics biodegradation and metabolism'},
        { 'Xylene degradation': 'Xenobiotics biodegradation and metabolism'},
        { 'Nitrotoluene degradation': 'Xenobiotics biodegradation and metabolism'},
        { 'Ethylbenzene degradation': 'Xenobiotics biodegradation and metabolism'},
        { 'Styrene degradation': 'Xenobiotics biodegradation and metabolism'},
        { 'Atrazine degradation': 'Xenobiotics biodegradation and metabolism'},
        { 'Caprolactam degradation': 'Xenobiotics biodegradation and metabolism'},
        { 'Bisphenol degradation': 'Xenobiotics biodegradation and metabolism'},
        { 'Dioxin degradation': 'Xenobiotics biodegradation and metabolism'},
        { 'Naphthalene degradation': 'Xenobiotics biodegradation and metabolism'},
        { 'Polycyclic aromatic hydrocarbon degradation': 'Xenobiotics biodegradation and metabolism'},
        { 'Furfural degradation': 'Xenobiotics biodegradation and metabolism'},
        { 'Steroid degradation': 'Xenobiotics biodegradation and metabolism'},
        { 'Metabolism of xenobiotics by cytochrome P450': 'Xenobiotics biodegradation and metabolism'},
        { 'Drug metabolism - cytochrome P450': 'Xenobiotics biodegradation and metabolism'},
        { 'Drug metabolism - other enzymes': 'Xenobiotics biodegradation and metabolism'},
        { 'Overview of biosynthetic pathways': 'Chemical structure transformation maps'},
        { 'Biosynthesis of plant secondary metabolites': 'Chemical structure transformation maps'},
        { 'Biosynthesis of phenylpropanoids': 'Chemical structure transformation maps'},
        { 'Biosynthesis of terpenoids and steroids': 'Chemical structure transformation maps'},
        { 'Biosynthesis of alkaloids derived from shikimate pathway': 'Chemical structure transformation maps'},
        { 'Biosynthesis of alkaloids derived from ornithine, lysine and nicotinic acid': 'Chemical structure transformation maps'},
        { 'Biosynthesis of alkaloids derived from histidine and purine': 'Chemical structure transformation maps'},
        { 'Biosynthesis of alkaloids derived from terpenoid and polyketide': 'Chemical structure transformation maps'},
        { 'Biosynthesis of plant hormones': 'Chemical structure transformation maps'},
        { 'RNA polymerase': 'Transcription'},
        { 'Basal transcription factors': 'Transcription'},
        { 'Spliceosome': 'Transcription'},
        { 'Ribosome': 'Translation'},
        { 'Aminoacyl-tRNA biosynthesis': 'Translation'},
        { 'RNA transport': 'Translation'},
        { 'mRNA surveillance pathway': 'Translation'},
        { 'Ribosome biogenesis in eukaryotes': 'Translation'},
        { 'Protein export': 'Folding, sorting and degradation'},
        { 'Protein processing in endoplasmic reticulum': 'Folding, sorting and degradation'},
        { 'SNARE interactions in vesicular transport': 'Folding, sorting and degradation'},
        { 'Ubiquitin mediated proteolysis': 'Folding, sorting and degradation'},
        { 'Sulfur relay system': 'Folding, sorting and degradation'},
        { 'Proteasome': 'Folding, sorting and degradation'},
        { 'RNA degradation': 'Folding, sorting and degradation'},
        { 'DNA replication': 'Replication and repair'},
        { 'Base excision repair': 'Replication and repair'},
        { 'Nucleotide excision repair': 'Replication and repair'},
        { 'Mismatch repair': 'Replication and repair'},
        { 'Homologous recombination': 'Replication and repair'},
        { 'Non-homologous end-joining': 'Replication and repair'},
        { 'Fanconi anemia pathway': 'Replication and repair'},
        { 'ABC transporters': 'Membrane transport'},
        { 'Phosphotransferase system (PTS)': 'Membrane transport'},
        { 'Bacterial secretion system': 'Membrane transport'},
        { 'Two-component system': 'Signal transduction'},
        { 'Ras signaling pathway': 'Signal transduction'},
        { 'Rap1 signaling pathway': 'Signal transduction'},
        { 'MAPK signaling pathway': 'Signal transduction'},
        { 'MAPK signaling pathway - fly': 'Signal transduction'},
        { 'MAPK signaling pathway - plant': 'Signal transduction'},
        { 'MAPK signaling pathway - yeast': 'Signal transduction'},
        { 'ErbB signaling pathway': 'Signal transduction'},
        { 'Wnt signaling pathway': 'Signal transduction'},
        { 'Notch signaling pathway': 'Signal transduction'},
        { 'Hedgehog signaling pathway': 'Signal transduction'},
        { 'Hedgehog signaling pathway - fly': 'Signal transduction'},
        { 'TGF-beta signaling pathway': 'Signal transduction'},
        { 'Hippo signaling pathway': 'Signal transduction'},
        { 'Hippo signaling pathway - fly': 'Signal transduction'},
        { 'Hippo signaling pathway - multiple species': 'Signal transduction'},
        { 'VEGF signaling pathway': 'Signal transduction'},
        { 'Apelin signaling pathway': 'Signal transduction'},
        { 'JAK-STAT signaling pathway': 'Signal transduction'},
        { 'NF-kappa B signaling pathway': 'Signal transduction'},
        { 'TNF signaling pathway': 'Signal transduction'},
        { 'HIF-1 signaling pathway': 'Signal transduction'},
        { 'FoxO signaling pathway': 'Signal transduction'},
        { 'Calcium signaling pathway': 'Signal transduction'},
        { 'Phosphatidylinositol signaling system': 'Signal transduction'},
        { 'Phospholipase D signaling pathway': 'Signal transduction'},
        { 'Sphingolipid signaling pathway': 'Signal transduction'},
        { 'cAMP signaling pathway': 'Signal transduction'},
        { 'cGMP-PKG signaling pathway': 'Signal transduction'},
        { 'PI3K-Akt signaling pathway': 'Signal transduction'},
        { 'AMPK signaling pathway': 'Signal transduction'},
        { 'mTOR signaling pathway': 'Signal transduction'},
        { 'Plant hormone signal transduction': 'Signal transduction'},
        { 'Neuroactive ligand-receptor interaction': 'Signaling molecules and interaction'},
        { 'Cytokine-cytokine receptor interaction': 'Signaling molecules and interaction'},
        { 'Viral protein interaction with cytokine and cytokine receptor': 'Signaling molecules and interaction'},
        { 'ECM-receptor interaction': 'Signaling molecules and interaction'},
        { 'Cell adhesion molecules': 'Signaling molecules and interaction'},
        { 'Endocytosis': 'Transport and catabolism'},
        { 'Phagosome': 'Transport and catabolism'},
        { 'Lysosome': 'Transport and catabolism'},
        { 'Peroxisome': 'Transport and catabolism'},
        { 'Autophagy - animal': 'Transport and catabolism'},
        { 'Autophagy - yeast': 'Transport and catabolism'},
        { 'Autophagy - other': 'Transport and catabolism'},
        { 'Mitophagy - animal': 'Transport and catabolism'},
        { 'Mitophagy - yeast': 'Transport and catabolism'},
        { 'Cell cycle': 'Cell growth and death'},
        { 'Cell cycle - yeast': 'Cell growth and death'},
        { 'Cell cycle - Caulobacter': 'Cell growth and death'},
        { 'Meiosis - yeast': 'Cell growth and death'},
        { 'Oocyte meiosis': 'Cell growth and death'},
        { 'Apoptosis': 'Cell growth and death'},
        { 'Apoptosis - fly': 'Cell growth and death'},
        { 'Apoptosis - multiple species': 'Cell growth and death'},
        { 'Ferroptosis': 'Cell growth and death'},
        { 'Necroptosis': 'Cell growth and death'},
        { 'p53 signaling pathway': 'Cell growth and death'},
        { 'Cellular senescence': 'Cell growth and death'},
        { 'Focal adhesion': 'Cellular community - eukaryotes'},
        { 'Adherens junction': 'Cellular community - eukaryotes'},
        { 'Tight junction': 'Cellular community - eukaryotes'},
        { 'Gap junction': 'Cellular community - eukaryotes'},
        { 'Signaling pathways regulating pluripotency of stem cells': 'Cellular community - eukaryotes'},
        { 'Quorum sensing': 'Cellular community - prokaryotes'},
        { 'Biofilm formation - Vibrio cholerae': 'Cellular community - prokaryotes'},
        { 'Biofilm formation - Pseudomonas aeruginosa': 'Cellular community - prokaryotes'},
        { 'Biofilm formation - Escherichia coli': 'Cellular community - prokaryotes'},
        { 'Bacterial chemotaxis': 'Cell motility'},
        { 'Flagellar assembly': 'Cell motility'},
        { 'Regulation of actin cytoskeleton': 'Cell motility'},
        { 'Hematopoietic cell lineage': 'Immune system'},
        { 'Complement and coagulation cascades': 'Immune system'},
        { 'Platelet activation': 'Immune system'},
        { 'Toll-like receptor signaling pathway': 'Immune system'},
        { 'Toll and Imd signaling pathway': 'Immune system'},
        { 'NOD-like receptor signaling pathway': 'Immune system'},
        { 'RIG-I-like receptor signaling pathway': 'Immune system'},
        { 'Cytosolic DNA-sensing pathway': 'Immune system'},
        { 'C-type lectin receptor signaling pathway': 'Immune system'},
        { 'Natural killer cell mediated cytotoxicity': 'Immune system'},
        { 'Antigen processing and presentation': 'Immune system'},
        { 'T cell receptor signaling pathway': 'Immune system'},
        { 'Th1 and Th2 cell differentiation': 'Immune system'},
        { 'Th17 cell differentiation': 'Immune system'},
        { 'IL-17 signaling pathway': 'Immune system'},
        { 'B cell receptor signaling pathway': 'Immune system'},
        { 'Fc epsilon RI signaling pathway': 'Immune system'},
        { 'Fc gamma R-mediated phagocytosis': 'Immune system'},
        { 'Leukocyte transendothelial migration': 'Immune system'},
        { 'Intestinal immune network for IgA production': 'Immune system'},
        { 'Chemokine signaling pathway': 'Immune system'},
        { 'Insulin secretion': 'Endocrine system'},
        { 'Insulin signaling pathway': 'Endocrine system'},
        { 'Glucagon signaling pathway': 'Endocrine system'},
        { 'Regulation of lipolysis in adipocytes': 'Endocrine system'},
        { 'Adipocytokine signaling pathway': 'Endocrine system'},
        { 'PPAR signaling pathway': 'Endocrine system'},
        { 'GnRH secretion': 'Endocrine system'},
        { 'GnRH signaling pathway': 'Endocrine system'},
        { 'Ovarian steroidogenesis': 'Endocrine system'},
        { 'Estrogen signaling pathway': 'Endocrine system'},
        { 'Progesterone-mediated oocyte maturation': 'Endocrine system'},
        { 'Prolactin signaling pathway': 'Endocrine system'},
        { 'Oxytocin signaling pathway': 'Endocrine system'},
        { 'Relaxin signaling pathway': 'Endocrine system'},
        { 'Growth hormone synthesis, secretion and action': 'Endocrine system'},
        { 'Thyroid hormone synthesis': 'Endocrine system'},
        { 'Thyroid hormone signaling pathway': 'Endocrine system'},
        { 'Parathyroid hormone synthesis, secretion and action': 'Endocrine system'},
        { 'Melanogenesis': 'Endocrine system'},
        { 'Renin secretion': 'Endocrine system'},
        { 'Renin-angiotensin system': 'Endocrine system'},
        { 'Aldosterone synthesis and secretion': 'Endocrine system'},
        { 'Cortisol synthesis and secretion': 'Endocrine system'},
        { 'Cardiac muscle contraction': 'Circulatory system'},
        { 'Adrenergic signaling in cardiomyocytes': 'Circulatory system'},
        { 'Vascular smooth muscle contraction': 'Circulatory system'},
        { 'Salivary secretion': 'Digestive system'},
        { 'Gastric acid secretion': 'Digestive system'},
        { 'Pancreatic secretion': 'Digestive system'},
        { 'Bile secretion': 'Digestive system'},
        { 'Carbohydrate digestion and absorption': 'Digestive system'},
        { 'Protein digestion and absorption': 'Digestive system'},
        { 'Fat digestion and absorption': 'Digestive system'},
        { 'Cholesterol metabolism': 'Digestive system'},
        { 'Vitamin digestion and absorption': 'Digestive system'},
        { 'Mineral absorption': 'Digestive system'},
        { 'Vasopressin-regulated water reabsorption': 'Excretory system'},
        { 'Aldosterone-regulated sodium reabsorption': 'Excretory system'},
        { 'Endocrine and other factor-regulated calcium reabsorption': 'Excretory system'},
        { 'Proximal tubule bicarbonate reclamation': 'Excretory system'},
        { 'Collecting duct acid secretion': 'Excretory system'},
        { 'Glutamatergic synapse': 'Nervous system'},
        { 'GABAergic synapse': 'Nervous system'},
        { 'Cholinergic synapse': 'Nervous system'},
        { 'Dopaminergic synapse': 'Nervous system'},
        { 'Serotonergic synapse': 'Nervous system'},
        { 'Long-term potentiation': 'Nervous system'},
        { 'Long-term depression': 'Nervous system'},
        { 'Retrograde endocannabinoid signaling': 'Nervous system'},
        { 'Synaptic vesicle cycle': 'Nervous system'},
        { 'Neurotrophin signaling pathway': 'Nervous system'},
        { 'Phototransduction': 'Sensory system'},
        { 'Phototransduction - fly': 'Sensory system'},
        { 'Olfactory transduction': 'Sensory system'},
        { 'Taste transduction': 'Sensory system'},
        { 'Inflammatory mediator regulation of TRP channels': 'Sensory system'},
        { 'Dorso-ventral axis formation': 'Development and regeneration'},
        { 'Axon guidance': 'Development and regeneration'},
        { 'Axon regeneration': 'Development and regeneration'},
        { 'Osteoclast differentiation': 'Development and regeneration'},
        { 'Longevity regulating pathway': 'Aging'},
        { 'Longevity regulating pathway - worm': 'Aging'},
        { 'Longevity regulating pathway - multiple species': 'Aging'},
        { 'Circadian rhythm': 'Environmental adaptation'},
        { 'Circadian entrainment': 'Environmental adaptation'},
        { 'Circadian rhythm - fly': 'Environmental adaptation'},
        { 'Circadian rhythm - plant': 'Environmental adaptation'},
        { 'Thermogenesis': 'Environmental adaptation'},
        { 'Plant-pathogen interaction': 'Environmental adaptation'},
        { 'Pathways in cancer': 'Cancer: overview'},
        { 'Transcriptional misregulation in cancer': 'Cancer: overview'},
        { 'MicroRNAs in cancer': 'Cancer: overview'},
        { 'Proteoglycans in cancer': 'Cancer: overview'},
        { 'Chemical carcinogenesis': 'Cancer: overview'},
        { 'Viral carcinogenesis': 'Cancer: overview'},
        { 'Central carbon metabolism in cancer': 'Cancer: overview'},
        { 'Choline metabolism in cancer': 'Cancer: overview'},
        { 'PD-L1 expression and PD-1 checkpoint pathway in cancer': 'Cancer: overview'},
        { 'Colorectal cancer': 'Cancer: specific types'},
        { 'Pancreatic cancer': 'Cancer: specific types'},
        { 'Hepatocellular carcinoma': 'Cancer: specific types'},
        { 'Gastric cancer': 'Cancer: specific types'},
        { 'Glioma': 'Cancer: specific types'},
        { 'Thyroid cancer': 'Cancer: specific types'},
        { 'Acute myeloid leukemia': 'Cancer: specific types'},
        { 'Chronic myeloid leukemia': 'Cancer: specific types'},
        { 'Basal cell carcinoma': 'Cancer: specific types'},
        { 'Melanoma': 'Cancer: specific types'},
        { 'Renal cell carcinoma': 'Cancer: specific types'},
        { 'Bladder cancer': 'Cancer: specific types'},
        { 'Prostate cancer': 'Cancer: specific types'},
        { 'Endometrial cancer': 'Cancer: specific types'},
        { 'Breast cancer': 'Cancer: specific types'},
        { 'Small cell lung cancer': 'Cancer: specific types'},
        { 'Non-small cell lung cancer': 'Cancer: specific types'},
        { 'Asthma': 'Immune disease'},
        { 'Systemic lupus erythematosus': 'Immune disease'},
        { 'Rheumatoid arthritis': 'Immune disease'},
        { 'Autoimmune thyroid disease': 'Immune disease'},
        { 'Inflammatory bowel disease': 'Immune disease'},
        { 'Allograft rejection': 'Immune disease'},
        { 'Graft-versus-host disease': 'Immune disease'},
        { 'Primary immunodeficiency': 'Immune disease'},
        { 'Alzheimer disease': 'Neurodegenerative disease'},
        { 'Parkinson disease': 'Neurodegenerative disease'},
        { 'Amyotrophic lateral sclerosis': 'Neurodegenerative disease'},
        { 'Huntington disease': 'Neurodegenerative disease'},
        { 'Spinocerebellar ataxia': 'Neurodegenerative disease'},
        { 'Prion diseases': 'Neurodegenerative disease'},
        { 'Cocaine addiction': 'Substance dependence'},
        { 'Amphetamine addiction': 'Substance dependence'},
        { 'Morphine addiction': 'Substance dependence'},
        { 'Nicotine addiction': 'Substance dependence'},
        { 'Alcoholism': 'Substance dependence'},
        { 'Fluid shear stress and atherosclerosis': 'Cardiovascular disease'},
        { 'Hypertrophic cardiomyopathy': 'Cardiovascular disease'},
        { 'Arrhythmogenic right ventricular cardiomyopathy': 'Cardiovascular disease'},
        { 'Dilated cardiomyopathy': 'Cardiovascular disease'},
        { 'Viral myocarditis': 'Cardiovascular disease'},
        { 'Type II diabetes mellitus': 'Endocrine and metabolic disease'},
        { 'Type I diabetes mellitus': 'Endocrine and metabolic disease'},
        { 'Maturity onset diabetes of the young': 'Endocrine and metabolic disease'},
        { 'Non-alcoholic fatty liver disease': 'Endocrine and metabolic disease'},
        { 'Insulin resistance': 'Endocrine and metabolic disease'},
        { 'AGE-RAGE signaling pathway in diabetic complications': 'Endocrine and metabolic disease'},
        { 'Cushing syndrome': 'Endocrine and metabolic disease'},
        { 'Vibrio cholerae infection': 'Infectious disease: bacterial'},
        { 'Epithelial cell signaling in Helicobacter pylori infection': 'Infectious disease: bacterial'},
        { 'Pathogenic Escherichia coli infection': 'Infectious disease: bacterial'},
        { 'Salmonella infection': 'Infectious disease: bacterial'},
        { 'Shigellosis': 'Infectious disease: bacterial'},
        { 'Yersinia infection': 'Infectious disease: bacterial'},
        { 'Pertussis': 'Infectious disease: bacterial'},
        { 'Legionellosis': 'Infectious disease: bacterial'},
        { 'Staphylococcus aureus infection': 'Infectious disease: bacterial'},
        { 'Tuberculosis': 'Infectious disease: bacterial'},
        { 'Bacterial invasion of epithelial cells': 'Infectious disease: bacterial'},
        { 'Infectious disease: viral': 'Infectious disease: viral'},
        { 'Human immunodeficiency virus 1 infection': 'Infectious disease: viral'},
        { 'Measles': 'Infectious disease: viral'},
        { 'Influenza A': 'Infectious disease: viral'},
        { 'Hepatitis B': 'Infectious disease: viral'},
        { 'Hepatitis C': 'Infectious disease: viral'},
        { 'Herpes simplex virus 1 infection': 'Infectious disease: viral'},
        { 'Human cytomegalovirus infection': 'Infectious disease: viral'},
        { 'Kaposi sarcoma-associated herpesvirus infection': 'Infectious disease: viral'},
        { 'Epstein-Barr virus infection': 'Infectious disease: viral'},
        { 'Human papillomavirus infection': 'Infectious disease: viral'},
        { 'Amoebiasis': 'Infectious disease: parasitic'},
        { 'Malaria': 'Infectious disease: parasitic'},
        { 'Toxoplasmosis': 'Infectious disease: parasitic'},
        { 'Leishmaniasis': 'Infectious disease: parasitic'},
        { 'Chagas disease': 'Infectious disease: parasitic'},
        { 'African trypanosomiasis': 'Infectious disease: parasitic'},
        { 'beta-Lactam resistance': 'Drug resistance: antimicrobial'},
        { 'Vancomycin resistance': 'Drug resistance: antimicrobial'},
        { 'Cationic antimicrobial peptide (CAMP) resistance': 'Drug resistance: antimicrobial'},
        { 'EGFR tyrosine kinase inhibitor resistance': 'Drug resistance: antineoplastic'},
        { 'Platinum drug resistance': 'Drug resistance: antineoplastic'},
        { 'Antifolate resistance': 'Drug resistance: antineoplastic'},
        { 'Endocrine resistance': 'Drug resistance: antineoplastic'},
        { 'Penicillins': 'Chronology: Antiinfectives'},
        { 'Cephalosporins - parenteral agents': 'Chronology: Antiinfectives'},
        { 'Cephalosporins - oral agents': 'Chronology: Antiinfectives'},
        { 'Aminoglycosides': 'Chronology: Antiinfectives'},
        { 'Tetracyclines': 'Chronology: Antiinfectives'},
        { 'Macrolides and ketolides': 'Chronology: Antiinfectives'},
        { 'Quinolones': 'Chronology: Antiinfectives'},
        { 'Rifamycins': 'Chronology: Antiinfectives'},
        { 'Antifungal agents': 'Chronology: Antiinfectives'},
        { 'Antiviral agents': 'Chronology: Antiinfectives'},
        { 'Anti-HIV agents': 'Chronology: Antiinfectives'},
        { 'Antineoplastics - alkylating agents': 'Chronology: Antineoplastics'},
        { 'Antineoplastics - antimetabolic agents': 'Chronology: Antineoplastics'},
        { 'Antineoplastics - agents from natural products': 'Chronology: Antineoplastics'},
        { 'Antineoplastics - hormones': 'Chronology: Antineoplastics'},
        { 'Antineoplastics - protein kinase inhibitors': 'Chronology: Antineoplastics'},
        { 'Hypnotics': 'Chronology: Nervous system agents'},
        { 'Anxiolytics': 'Chronology: Nervous system agents'},
        { 'Anticonvulsants': 'Chronology: Nervous system agents'},
        { 'Local analgesics': 'Chronology: Nervous system agents'},
        { 'Opioid analgesics': 'Chronology: Nervous system agents'},
        { 'Antipsychotics': 'Chronology: Nervous system agents'},
        { 'Antipsychotics - phenothiazines': 'Chronology: Nervous system agents'},
        { 'Antipsychotics - butyrophenones': 'Chronology: Nervous system agents'},
        { 'Antidepressants': 'Chronology: Nervous system agents'},
        { 'Agents for Alzheimer-type dementia': 'Chronology: Nervous system agents'},
        { 'Antiparkinsonian agents': 'Chronology: Nervous system agents'},
        { 'Sulfonamide derivatives - overview': 'Chronology: Other drugs'},
        { 'Sulfonamide derivatives - sulfa drugs': 'Chronology: Other drugs'},
        { 'Sulfonamide derivatives - diuretics': 'Chronology: Other drugs'},
        { 'Sulfonamide derivatives - hypoglycemic agents': 'Chronology: Other drugs'},
        { 'Antiarrhythmic drugs': 'Chronology: Other drugs'},
        { 'Antiulcer drugs': 'Chronology: Other drugs'},
        { 'Immunosuppressive agents': 'Chronology: Other drugs'},
        { 'Osteoporosis drugs': 'Chronology: Other drugs'},
        { 'Antimigraines': 'Chronology: Other drugs'},
        { 'Antithrombosis agents': 'Chronology: Other drugs'},
        { 'Antirheumatics - DMARDs and biological agents': 'Chronology: Other drugs'},
        { 'Antidiabetics': 'Chronology: Other drugs'},
        { 'Antidyslipidemic agents': 'Chronology: Other drugs'},
        { 'Antiglaucoma agents': 'Chronology: Other drugs'},
        { 'Cholinergic and anticholinergic drugs': 'Target-based classification: G protein-coupled receptors'},
        { 'alpha-Adrenergic receptor agonists/antagonists': 'Target-based classification: G protein-coupled receptors'},
        { 'beta-Adrenergic receptor agonists/antagonists': 'Target-based classification: G protein-coupled receptors'},
        { 'Dopamine receptor agonists/antagonists': 'Target-based classification: G protein-coupled receptors'},
        { 'Histamine H1 receptor antagonists': 'Target-based classification: G protein-coupled receptors'},
        { 'Histamine H2/H3 receptor agonists/antagonists': 'Target-based classification: G protein-coupled receptors'},
        { 'Serotonin receptor agonists/antagonists': 'Target-based classification: G protein-coupled receptors'},
        { 'Eicosanoid receptor agonists/antagonists': 'Target-based classification: G protein-coupled receptors'},
        { 'Opioid receptor agonists/antagonists': 'Target-based classification: G protein-coupled receptors'},
        { 'Angiotensin receptor and endothelin receptor antagonists': 'Target-based classification: G protein-coupled receptors'},
        { 'Glucocorticoid and mineralocorticoid receptor agonists/antagonists': 'Target-based classification: Nuclear receptors'},
        { 'Progesterone, androgen and estrogen receptor agonists/antagonists': 'Target-based classification: Nuclear receptors'},
        { 'Retinoic acid receptor (RAR) and retinoid X receptor (RXR) agonists/antagonists': 'Target-based classification: Nuclear receptors'},
        { 'Peroxisome proliferator-activated receptor (PPAR) agonists': 'Target-based classification: Nuclear receptors'},
        { 'Nicotinic cholinergic receptor antagonists': 'Target-based classification: Ion channels'},
        { 'GABA-A receptor agonists/antagonists': 'Target-based classification: Ion channels'},
        { 'Calcium channel blocking drugs': 'Target-based classification: Ion channels'},
        { 'Sodium channel blocking drugs': 'Target-based classification: Ion channels'},
        { 'Potassium channel blocking and opening drugs': 'Target-based classification: Ion channels'},
        { 'N-Metyl-D-aspartic acid receptor antagonists': 'Target-based classification: Ion channels'},
        { 'Ion transporter inhibitors': 'Target-based classification: Transporters'},
        { 'Neurotransmitter transporter inhibitors': 'Target-based classification: Transporters'},
        { 'Catecholamine transferase inhibitors': 'Target-based classification: Enzymes'},
        { 'Cyclooxygenase inhibitors': 'Target-based classification: Enzymes'},
        { 'HMG-CoA reductase inhibitors': 'Target-based classification: Enzymes'},
        { 'Renin-angiotensin system inhibitors': 'Target-based classification: Enzymes'},
        { 'HIV protease inhibitors': 'Target-based classification: Enzymes'},
        { 'Quinolines': 'Structure-based classification'},
        { 'Eicosanoids': 'Structure-based classification'},
        { 'Prostaglandins': 'Structure-based classification'},
        { 'Benzoic acid family': 'Skeleton-based classification'},
        { '1,2-Diphenyl substitution family': 'Skeleton-based classification'},
        { 'Naphthalene family': 'Skeleton-based classification'},
        { 'Benzodiazepine family': 'Skeleton-based classification'}
        ]

