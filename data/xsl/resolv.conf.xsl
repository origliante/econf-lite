<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
  <xsl:output method="text"/>

  <xsl:template match="/">
    <xsl:apply-templates select="/network/dns"/>
  </xsl:template>

  <xsl:template match="dns">
    <xsl:text>#&#10;</xsl:text>
    <xsl:text># DNS resolver stuff&#10;</xsl:text>
    <xsl:text>#&#10;</xsl:text>

    <xsl:text>domain&#09;&#09;</xsl:text>
    <xsl:value-of select="@domain"/>
    <xsl:text>&#10;</xsl:text>

    <!-- non gestisce la precedenza dei domini locali -->
    <xsl:if test="search">
      <xsl:text>search&#09;&#09;</xsl:text>
      <xsl:for-each select="search">
        <xsl:value-of select="@domain"/>
        <xsl:text>&#09;</xsl:text>
      </xsl:for-each>
      <xsl:text>&#10;</xsl:text>
    </xsl:if>

    <xsl:for-each select="nameserver">
      <xsl:text>nameserver&#09;</xsl:text>
      <xsl:value-of select="@address"/>
      <xsl:text>&#10;</xsl:text>
    </xsl:for-each>
  </xsl:template>

</xsl:stylesheet>
