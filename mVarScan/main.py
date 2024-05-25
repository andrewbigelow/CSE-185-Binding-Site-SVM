
def main() :
    # Populate variables from command line tool
    mpileup = args.mpileup
    min_var_frequency = 0.2
    if args.min_var_frequency != None :
        min_var_frequency = args.min_var_frequency
    
    min_frequency_for_hom = 0.8
    if args.min_frequency_for_hom != None :
        min_frequency_for_hom = args.min_frequency_for_hom