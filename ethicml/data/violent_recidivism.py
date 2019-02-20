"""
Class to describe features of the Adult dataset
"""
from typing import Dict, List

from .dataset import Dataset
from .load import filter_features_by_prefixes


# Can't disable duplicate code warning on abstract methods, so disabling all for this file (for now)
# pylint: disable-all


class Violent(Dataset):
    features: List[str]
    y_prefix: List[str]
    y_labels: List[str]
    s_prefix: List[str]
    sens_attrs: List[str]
    _cont_features: List[str]
    _disc_features: List[str]

    def __init__(self, split: str = "Sex", discrete_only: bool = False):
        self.discrete_only = discrete_only
        self.features = [
            'sex',
            'age',
            'race',
            'juv_fel_count',
            'juv_misd_count',
            'juv_other_count',
            'priors_count',
            'two_year_recid',
            'age_cat_25 - 45',
            'age_cat_Greater than 45',
            'age_cat_Less than 25',
            'c_charge_degree_F',
            'c_charge_degree_M',
            'c_charge_desc_Abuse Without Great Harm',
            'c_charge_desc_Agg Abuse Elderlly/Disabled Adult',
            'c_charge_desc_Agg Assault W/int Com Fel Dome',
            'c_charge_desc_Agg Battery Grt/Bod/Harm',
            'c_charge_desc_Agg Fleeing and Eluding',
            'c_charge_desc_Agg Fleeing/Eluding High Speed',
            'c_charge_desc_Aggr Child Abuse-Torture,Punish',
            'c_charge_desc_Aggrav Battery w/Deadly Weapon',
            'c_charge_desc_Aggrav Child Abuse-Agg Battery',
            'c_charge_desc_Aggrav Child Abuse-Causes Harm',
            'c_charge_desc_Aggrav Stalking After Injunctn',
            'c_charge_desc_Aggravated Assault',
            'c_charge_desc_Aggravated Assault W/Dead Weap',
            'c_charge_desc_Aggravated Assault W/dead Weap',
            'c_charge_desc_Aggravated Assault W/o Firearm',
            'c_charge_desc_Aggravated Assault w/Firearm',
            'c_charge_desc_Aggravated Battery',
            'c_charge_desc_Aggravated Battery (Firearm)',
            'c_charge_desc_Aggravated Battery (Firearm/Actual Possession)',
            'c_charge_desc_Aggravated Battery / Pregnant',
            'c_charge_desc_Aggravated Battery On 65/Older',
            'c_charge_desc_Alcoholic Beverage Violation-FL',
            'c_charge_desc_Armed Trafficking in Cannabis',
            'c_charge_desc_Arson in the First Degree',
            'c_charge_desc_Assault',
            'c_charge_desc_Att Burgl Struc/Conv Dwel/Occp',
            'c_charge_desc_Att Burgl Unoccupied Dwel',
            'c_charge_desc_Att Tamper w/Physical Evidence',
            'c_charge_desc_Attempt Armed Burglary Dwell',
            'c_charge_desc_Attempted Robbery  No Weapon',
            'c_charge_desc_Battery',
            'c_charge_desc_Battery On Fire Fighter',
            'c_charge_desc_Battery On Parking Enfor Speci',
            'c_charge_desc_Battery Spouse Or Girlfriend',
            'c_charge_desc_Battery on Law Enforc Officer',
            'c_charge_desc_Battery on a Person Over 65',
            'c_charge_desc_Bribery Athletic Contests',
            'c_charge_desc_Burglary Assault/Battery Armed',
            'c_charge_desc_Burglary Conveyance Armed',
            'c_charge_desc_Burglary Conveyance Assault/Bat',
            'c_charge_desc_Burglary Conveyance Occupied',
            'c_charge_desc_Burglary Conveyance Unoccup',
            'c_charge_desc_Burglary Dwelling Armed',
            'c_charge_desc_Burglary Dwelling Assault/Batt',
            'c_charge_desc_Burglary Dwelling Occupied',
            'c_charge_desc_Burglary Structure Assault/Batt',
            'c_charge_desc_Burglary Structure Occupied',
            'c_charge_desc_Burglary Structure Unoccup',
            'c_charge_desc_Burglary Unoccupied Dwelling',
            'c_charge_desc_Burglary With Assault/battery',
            'c_charge_desc_Carjacking w/o Deadly Weapon',
            'c_charge_desc_Carjacking with a Firearm',
            'c_charge_desc_Carry Open/Uncov Bev In Pub',
            'c_charge_desc_Carrying Concealed Firearm',
            'c_charge_desc_Cash Item w/Intent to Defraud',
            'c_charge_desc_Child Abuse',
            'c_charge_desc_Computer Pornography',
            'c_charge_desc_Consp Traff Oxycodone  4g><14g',
            'c_charge_desc_Conspiracy Dealing Stolen Prop',
            'c_charge_desc_Consume Alcoholic Bev Pub',
            'c_charge_desc_Contribute Delinquency Of A Minor',
            'c_charge_desc_Corrupt Public Servant',
            'c_charge_desc_Counterfeit Lic Plates/Sticker',
            'c_charge_desc_Crim Use of Personal ID Info',
            'c_charge_desc_Crimin Mischief Damage $1000+',
            'c_charge_desc_Criminal Mischief',
            'c_charge_desc_Criminal Mischief Damage <$200',
            'c_charge_desc_Criminal Mischief>$200<$1000',
            'c_charge_desc_Cruelty Toward Child',
            'c_charge_desc_Cruelty to Animals',
            'c_charge_desc_Culpable Negligence',
            'c_charge_desc_D.U.I. Serious Bodily Injury',
            'c_charge_desc_DOC/Cause Public Danger',
            'c_charge_desc_DUI - Enhanced',
            'c_charge_desc_DUI - Property Damage/Personal Injury',
            'c_charge_desc_DUI Blood Alcohol Above 0.20',
            'c_charge_desc_DUI Level 0.15 Or Minor In Veh',
            'c_charge_desc_DUI Property Damage/Injury',
            'c_charge_desc_DUI- Enhanced',
            'c_charge_desc_DUI/Property Damage/Persnl Inj',
            'c_charge_desc_DWI w/Inj Susp Lic / Habit Off',
            'c_charge_desc_DWLS Canceled Disqul 1st Off',
            'c_charge_desc_DWLS Susp/Cancel Revoked',
            'c_charge_desc_Dealing in Stolen Property',
            'c_charge_desc_Del 3,4 Methylenedioxymethcath',
            'c_charge_desc_Del Cannabis For Consideration',
            'c_charge_desc_Del of JWH-250 2-Methox 1-Pentyl',
            'c_charge_desc_Deliver 3,4 Methylenediox',
            'c_charge_desc_Deliver Alprazolam',
            'c_charge_desc_Deliver Cannabis',
            'c_charge_desc_Deliver Cannabis 1000FTSch',
            'c_charge_desc_Deliver Cocaine',
            'c_charge_desc_Deliver Cocaine 1000FT Park',
            'c_charge_desc_Deliver Cocaine 1000FT Store',
            'c_charge_desc_Delivery Of Drug Paraphernalia',
            'c_charge_desc_Delivery of 5-Fluoro PB-22',
            'c_charge_desc_Depriv LEO of Protect/Communic',
            'c_charge_desc_Disorderly Conduct',
            'c_charge_desc_Disorderly Intoxication',
            'c_charge_desc_Disrupting School Function',
            'c_charge_desc_Drivg While Lic Suspd/Revk/Can',
            'c_charge_desc_Driving License Suspended',
            'c_charge_desc_Driving Under The Influence',
            'c_charge_desc_Driving While License Revoked',
            'c_charge_desc_Escape',
            'c_charge_desc_Expired DL More Than 6 Months',
            'c_charge_desc_Exposes Culpable Negligence',
            'c_charge_desc_Extradition/Defendants',
            'c_charge_desc_Fail Register Vehicle',
            'c_charge_desc_Fail Sex Offend Report Bylaw',
            'c_charge_desc_Fail To Obey Police Officer',
            'c_charge_desc_Fail To Redeliv Hire/Leas Prop',
            'c_charge_desc_Failure To Pay Taxi Cab Charge',
            'c_charge_desc_Failure To Return Hired Vehicle',
            'c_charge_desc_False 911 Call',
            'c_charge_desc_False Bomb Report',
            'c_charge_desc_False Imprisonment',
            'c_charge_desc_False Info LEO During Invest',
            'c_charge_desc_False Motor Veh Insurance Card',
            'c_charge_desc_False Ownership Info/Pawn Item',
            'c_charge_desc_Falsely Impersonating Officer',
            'c_charge_desc_Fel Drive License Perm Revoke',
            'c_charge_desc_Felony Batt(Great Bodily Harm)',
            'c_charge_desc_Felony Battery',
            'c_charge_desc_Felony Battery (Dom Strang)',
            'c_charge_desc_Felony Battery w/Prior Convict',
            'c_charge_desc_Felony DUI (level 3)',
            'c_charge_desc_Felony DUI - Enhanced',
            'c_charge_desc_Felony Driving While Lic Suspd',
            'c_charge_desc_Felony Petit Theft',
            'c_charge_desc_Felony/Driving Under Influence',
            'c_charge_desc_Fighting/Baiting Animals',
            'c_charge_desc_Fleeing Or Attmp Eluding A Leo',
            'c_charge_desc_Fleeing or Eluding a LEO',
            'c_charge_desc_Forging Bank Bills/Promis Note',
            'c_charge_desc_Fraudulent Use of Credit Card',
            'c_charge_desc_Grand Theft (Motor Vehicle)',
            'c_charge_desc_Grand Theft Dwell Property',
            'c_charge_desc_Grand Theft Firearm',
            'c_charge_desc_Grand Theft in the 1st Degree',
            'c_charge_desc_Grand Theft in the 3rd Degree',
            'c_charge_desc_Grand Theft of a Fire Extinquisher',
            'c_charge_desc_Grand Theft of the 2nd Degree',
            'c_charge_desc_Grand Theft on 65 Yr or Older',
            'c_charge_desc_Harass Witness/Victm/Informnt',
            'c_charge_desc_Harm Public Servant Or Family',
            'c_charge_desc_Hiring with Intent to Defraud',
            'c_charge_desc_Interfere W/Traf Cont Dev RR',
            'c_charge_desc_Intoxicated/Safety Of Another',
            'c_charge_desc_Introduce Contraband Into Jail',
            'c_charge_desc_Kidnapping / Domestic Violence',
            'c_charge_desc_Lease For Purpose Trafficking',
            'c_charge_desc_Leave Acc/Attend Veh/More $50',
            'c_charge_desc_Leave Accd/Attend Veh/Less $50',
            'c_charge_desc_Leaving Acc/Unattended Veh',
            'c_charge_desc_Leaving the Scene of Accident',
            'c_charge_desc_Lewd Act Presence Child 16-',
            'c_charge_desc_Lewd or Lascivious Molestation',
            'c_charge_desc_Lewd/Lasc Battery Pers 12+/<16',
            'c_charge_desc_Lewd/Lasc Exhib Presence <16yr',
            'c_charge_desc_Lewd/Lasciv Molest Elder Persn',
            'c_charge_desc_Lewdness Violation',
            'c_charge_desc_License Suspended Revoked',
            'c_charge_desc_Live on Earnings of Prostitute',
            'c_charge_desc_Lve/Scen/Acc/Veh/Prop/Damage',
            'c_charge_desc_Manage Busn W/O City Occup Lic',
            'c_charge_desc_Manufacture Cannabis',
            'c_charge_desc_Misuse Of 911 Or E911 System',
            'c_charge_desc_Money Launder 100K or More Dols',
            'c_charge_desc_Murder In 2nd Degree W/firearm',
            'c_charge_desc_Murder in the First Degree',
            'c_charge_desc_Neglect Child / Bodily Harm',
            'c_charge_desc_Neglect Child / No Bodily Harm',
            'c_charge_desc_Neglect/Abuse Elderly Person',
            'c_charge_desc_Obstruct Fire Equipment',
            'c_charge_desc_Obtain Control Substance By Fraud',
            'c_charge_desc_Offer Agree Secure For Lewd Act',
            'c_charge_desc_Offer Agree Secure/Lewd Act',
            'c_charge_desc_Offn Against Intellectual Prop',
            'c_charge_desc_Open Carrying Of Weapon',
            'c_charge_desc_Oper Motorcycle W/O Valid DL',
            'c_charge_desc_Operating W/O Valid License',
            'c_charge_desc_Opert With Susp DL 2nd Offens',
            'c_charge_desc_Petit Theft',
            'c_charge_desc_Petit Theft $100- $300',
            'c_charge_desc_Pos Cannabis W/Intent Sel/Del',
            'c_charge_desc_Poss 3,4 MDMA (Ecstasy)',
            'c_charge_desc_Poss Anti-Shoplifting Device',
            'c_charge_desc_Poss Cocaine/Intent To Del/Sel',
            'c_charge_desc_Poss Contr Subst W/o Prescript',
            'c_charge_desc_Poss Drugs W/O A Prescription',
            'c_charge_desc_Poss F/Arm Delinq',
            'c_charge_desc_Poss Meth/Diox/Meth/Amp (MDMA)',
            'c_charge_desc_Poss Of Controlled Substance',
            'c_charge_desc_Poss Of RX Without RX',
            'c_charge_desc_Poss Oxycodone W/Int/Sell/Del',
            'c_charge_desc_Poss Pyrrolidinovalerophenone',
            'c_charge_desc_Poss Similitude of Drivers Lic',
            'c_charge_desc_Poss Tetrahydrocannabinols',
            'c_charge_desc_Poss Unlaw Issue Driver Licenc',
            'c_charge_desc_Poss Unlaw Issue Id',
            'c_charge_desc_Poss Wep Conv Felon',
            'c_charge_desc_Poss of Cocaine W/I/D/S 1000FT Park',
            'c_charge_desc_Poss of Firearm by Convic Felo',
            'c_charge_desc_Poss of Methylethcathinone',
            'c_charge_desc_Poss/Sell/Del Cocaine 1000FT Sch',
            'c_charge_desc_Poss3,4 Methylenedioxymethcath',
            'c_charge_desc_Posses/Disply Susp/Revk/Frd DL',
            'c_charge_desc_Possess Cannabis 1000FTSch',
            'c_charge_desc_Possess Cannabis/20 Grams Or Less',
            'c_charge_desc_Possess Controlled Substance',
            'c_charge_desc_Possess Drug Paraphernalia',
            'c_charge_desc_Possess Tobacco Product Under 18',
            'c_charge_desc_Possess Weapon On School Prop',
            'c_charge_desc_Possess w/I/Utter Forged Bills',
            'c_charge_desc_Possession Burglary Tools',
            'c_charge_desc_Possession Child Pornography',
            'c_charge_desc_Possession Firearm School Prop',
            'c_charge_desc_Possession Of 3,4Methylenediox',
            'c_charge_desc_Possession Of Alprazolam',
            'c_charge_desc_Possession Of Amphetamine',
            'c_charge_desc_Possession Of Anabolic Steroid',
            'c_charge_desc_Possession Of Buprenorphine',
            'c_charge_desc_Possession Of Diazepam',
            'c_charge_desc_Possession Of Fentanyl',
            'c_charge_desc_Possession Of Heroin',
            'c_charge_desc_Possession Of Methamphetamine',
            'c_charge_desc_Possession Of Paraphernalia',
            'c_charge_desc_Possession Of Phentermine',
            'c_charge_desc_Possession of Benzylpiperazine',
            'c_charge_desc_Possession of Cannabis',
            'c_charge_desc_Possession of Cocaine',
            'c_charge_desc_Possession of Codeine',
            'c_charge_desc_Possession of Hydrocodone',
            'c_charge_desc_Possession of Hydromorphone',
            'c_charge_desc_Possession of LSD',
            'c_charge_desc_Possession of Morphine',
            'c_charge_desc_Possession of Oxycodone',
            'c_charge_desc_Principal In The First Degree',
            'c_charge_desc_Prostitution',
            'c_charge_desc_Prostitution/Lewd Act Assignation',
            'c_charge_desc_Prostitution/Lewdness/Assign',
            'c_charge_desc_Prowling/Loitering',
            'c_charge_desc_Purchase Cannabis',
            'c_charge_desc_Purchase/P/W/Int Cannabis',
            'c_charge_desc_Reckless Driving',
            'c_charge_desc_Refuse Submit Blood/Breath Test',
            'c_charge_desc_Refuse to Supply DNA Sample',
            'c_charge_desc_Resist Officer w/Violence',
            'c_charge_desc_Resist/Obstruct W/O Violence',
            'c_charge_desc_Retail Theft $300 1st Offense',
            'c_charge_desc_Robbery / No Weapon',
            'c_charge_desc_Robbery / Weapon',
            'c_charge_desc_Robbery Sudd Snatch No Weapon',
            'c_charge_desc_Robbery W/Deadly Weapon',
            'c_charge_desc_Robbery W/Firearm',
            'c_charge_desc_Sale/Del Cannabis At/Near Scho',
            'c_charge_desc_Sale/Del Counterfeit Cont Subs',
            'c_charge_desc_Sel/Pur/Mfr/Del Control Substa',
            'c_charge_desc_Sell or Offer for Sale Counterfeit Goods',
            'c_charge_desc_Sex Battery Deft 18+/Vict 11-',
            'c_charge_desc_Sex Offender Fail Comply W/Law',
            'c_charge_desc_Sexual Battery / Vict 12 Yrs +',
            'c_charge_desc_Sexual Performance by a Child',
            'c_charge_desc_Shoot In Occupied Dwell',
            'c_charge_desc_Simulation of Legal Process',
            'c_charge_desc_Solic to Commit Battery',
            'c_charge_desc_Solicit Deliver Cocaine',
            'c_charge_desc_Solicit To Deliver Cocaine',
            'c_charge_desc_Solicitation On Felony 3 Deg',
            'c_charge_desc_Soliciting For Prostitution',
            'c_charge_desc_Stalking (Aggravated)',
            'c_charge_desc_Strong Armed  Robbery',
            'c_charge_desc_Structuring Transactions',
            'c_charge_desc_Susp Drivers Lic 1st Offense',
            'c_charge_desc_Tamper With Victim',
            'c_charge_desc_Tamper With Witness',
            'c_charge_desc_Tamper With Witness/Victim/CI',
            'c_charge_desc_Tampering With Physical Evidence',
            'c_charge_desc_Tampering with a Victim',
            'c_charge_desc_Theft/To Deprive',
            'c_charge_desc_Threat Public Servant',
            'c_charge_desc_Throw Deadly Missile Into Veh',
            'c_charge_desc_Throw In Occupied Dwell',
            'c_charge_desc_Throw Missile Into Pub/Priv Dw',
            'c_charge_desc_Traffick Amphetamine 28g><200g',
            'c_charge_desc_Traffick Oxycodone     4g><14g',
            'c_charge_desc_Trespass Property w/Dang Weap',
            'c_charge_desc_Trespass Structure/Conveyance',
            'c_charge_desc_Trespassing/Construction Site',
            'c_charge_desc_Tresspass Struct/Conveyance',
            'c_charge_desc_Tresspass in Structure or Conveyance',
            'c_charge_desc_Unauth C/P/S Sounds>1000/Audio',
            'c_charge_desc_Unauth Poss ID Card or DL',
            'c_charge_desc_Unl/Disturb Education/Instui',
            'c_charge_desc_Unlaw LicTag/Sticker Attach',
            'c_charge_desc_Unlaw Use False Name/Identity',
            'c_charge_desc_Unlawful Conveyance of Fuel',
            'c_charge_desc_Unlicensed Telemarketing',
            'c_charge_desc_Use Computer for Child Exploit',
            'c_charge_desc_Use Of 2 Way Device To Fac Fel',
            'c_charge_desc_Use Scanning Device to Defraud',
            'c_charge_desc_Use of Anti-Shoplifting Device',
            'c_charge_desc_Uttering Forged Bills',
            'c_charge_desc_Uttering Forged Credit Card',
            'c_charge_desc_Uttering a Forged Instrument',
            'c_charge_desc_Video Voyeur-<24Y on Child >16',
            'c_charge_desc_Viol Injunct Domestic Violence',
            'c_charge_desc_Viol Injunction Protect Dom Vi',
            'c_charge_desc_Viol Pretrial Release Dom Viol',
            'c_charge_desc_Viol Prot Injunc Repeat Viol',
            'c_charge_desc_Violation License Restrictions',
            'c_charge_desc_Violation Of Boater Safety Id',
            'c_charge_desc_Violation of Injunction Order/Stalking/Cyberstalking',
            'c_charge_desc_arrest case no charge'
        ]

        self._cont_features = [
            'age',
            'juv_fel_count',
            'juv_misd_count',
            'juv_other_count',
            'priors_count'
        ]

        if split == "Sex":
            self.sens_attrs = ['sex']
            self.s_prefix = ['sex']
            self.y_labels = ['two_year_recid']
            self.y_prefix = ['two_year_recid']
        elif split == "Race":
            self.sens_attrs = ['race']
            self.s_prefix = ['race']
            self.y_labels = ['two_year_recid']
            self.y_prefix = ['two_year_recid']
        elif split == "Race-Sex":
            self.sens_attrs = ['sex',
                               'race']
            self.s_prefix = ['race', 'sex']
            self.y_labels = ['two_year_recid']
            self.y_prefix = ['two_year_recid']
        else:
            raise NotImplementedError

        self.conc_features: List[str] = self.s_prefix + self.y_prefix
        self._disc_features = [item for item in filter_features_by_prefixes(self.features, self.conc_features)
                               if item not in self._cont_features]

    @property
    def name(self) -> str:
        return "Violent"

    @property
    def filename(self) -> str:
        return "violent_recidivism.csv"

    @property
    def feature_split(self) -> Dict[str, List[str]]:

        conc_features: List[str]
        if self.discrete_only:
            conc_features = self.s_prefix + self.y_prefix + self.continuous_features
        else:
            conc_features = self.s_prefix + self.y_prefix

        return {
            "x": filter_features_by_prefixes(self.features, conc_features),
            "s": self.sens_attrs,
            "y": self.y_labels
        }

    def set_s(self, sens_attrs: List[str]):
        self.sens_attrs = sens_attrs

    def set_s_prefix(self, sens_attr_prefixs: List[str]):
        self.s_prefix = sens_attr_prefixs

    def set_y(self, labels: List[str]):
        self.y_labels = labels

    def set_y_prefix(self, label_prefixs):
        self.y_prefix = label_prefixs

    @property
    def continuous_features(self) -> List[str]:
        return self._cont_features

    @property
    def discrete_features(self) -> List[str]:
        return self._disc_features
