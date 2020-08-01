class CompanyMixinViewSet:
    def get_queryset(self):
        if not self.queryset:
            raise Exception(
                "CompanyMixinViewSet must define queryset properties"
            )
        return self.queryset.filter(company=self.request.company)
